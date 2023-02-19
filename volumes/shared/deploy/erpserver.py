#!/usr/bin/env python3
# Taken from trytond/bin/trytond.
# PYTHON_ARGCOMPLETE_OK
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import glob
import logging
import os
import sys
import threading

try:
    import argcomplete
except ImportError:
    argcomplete = None

DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import trytond.commandline as commandline
from trytond.config import config, split_netloc

parser = commandline.get_parser_daemon()
if argcomplete:
    argcomplete.autocomplete(parser)
options = parser.parse_args()
commandline.config_log(options)
extra_files = config.update_etc(options.configfile)

if options.coroutine:
    # Monkey patching must be done before importing
    from gevent import monkey
    monkey.patch_all()

from trytond.modules import get_module_info, get_module_list
from trytond.pool import Pool
# Import trytond things after it is configured
from trytond.wsgi import app

with commandline.pidfile(options):
    Pool.start()
    threads = []
    for name in options.database_names:
        thread = threading.Thread(target=Pool(name).init)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    hostname, port = split_netloc(config.get('web', 'listen'))
    certificate = config.get('ssl', 'certificate')
    try:
        if config.getboolean('ssl', 'certificate'):
            certificate = None
    except ValueError:
        pass
    privatekey = config.get('ssl', 'privatekey')
    try:
        if config.getboolean('ssl', 'privatekey'):
            privatekey = None
    except ValueError:
        pass
    if certificate or privatekey:
        from werkzeug.serving import load_ssl_context
        ssl_args = dict(
            ssl_context=load_ssl_context(certificate, privatekey))
    else:
        ssl_args = {}
    if options.dev and not options.coroutine:
        for module in get_module_list():
            info = get_module_info(module)
            for ext in ['xml',
                    'fodt', 'odt', 'fodp', 'odp', 'fods', 'ods', 'fodg', 'odg',
                    'txt', 'html', 'xhtml']:
                path = os.path.join(info['directory'], '**', '*.' + ext)
                extra_files.extend(glob.glob(path, recursive=True))

    if options.coroutine:
        from gevent.pywsgi import WSGIServer
        logger = logging.getLogger('gevent')
        WSGIServer((hostname, port), app,
            log=logger,
            error_log=logger,
            **ssl_args).serve_forever()
    else:
        from werkzeug.serving import run_simple
        import ptvsd
        import socket

        try:
            ptvsd.enable_attach(address=("0.0.0.0", 51005), redirect_output=True)
        except socket.error as e:
            print(e)
            pass
        # ptvsd.wait_for_attach(); ptvsd.break_into_debugger()
        # threaded and use_realoader have to be false for ptvsd debugging
        run_simple(hostname, port, app,
            threaded=False,
            extra_files=extra_files,
            use_reloader=False,
            processes=1,
            **ssl_args)
