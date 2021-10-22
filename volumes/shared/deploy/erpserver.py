#!/usr/bin/env python
# EASY-INSTALL-DEV-SCRIPT: 'trytond==3.4.19','trytond'

import socket
import debugpy
# from trytond.config import config
# import trytond.commandline as commandline
# from trytond.tools import resolve

__requires__ = 'trytond'
__import__('pkg_resources').require('trytond')
__file__ = '/shared/src/trytond/bin/trytond'

from werkzeug import serving

serving._make_server = serving.make_server


def make_server(*args, **kwargs):
    try:
        debugpy.listen(("0.0.0.0", 51005))
        print("debugpy started.")
    except (RuntimeError, socket.error) as err:
        print("debugpy could not be started: " + err)
    return serving._make_server(*args, **kwargs)


serving.make_server = make_server
# parser = commandline.get_parser_admin()
# options = parser.parse_args()
# config.update_etc(options.configfile)

# from trytond import wsgi

# class DebugpyTrytondWSGI(wsgi.TrytondWSGI):
#     def __init__(self, *args, **kwargs):
#         try:
#             debugpy.listen(("0.0.0.0", 51005))
#             print("debugpy started.")
#         except (RuntimeError, socket.error) as err:
#             # print("waiting for debugpy client connection ...")
#             # debugpy.wait_for_client()
#             pass
#         super().__init__(*args, **kwargs)


# app = DebugpyTrytondWSGI()
# if config.get('web', 'root'):
#     static_files = {
#         '/': config.get('web', 'root'),
#         }
#     app.wsgi_app = wsgi.SharedDataMiddlewareIndex(
#         app.wsgi_app, static_files,
#         cache_timeout=config.getint('web', 'cache_timeout'))
# num_proxies = config.getint('web', 'num_proxies')
# if num_proxies:
#     app.wsgi_app = wsgi.NumProxyFix(app.wsgi_app, num_proxies)

# if config.has_section('wsgi middleware'):
#     for middleware in config.options('wsgi middleware'):
#         Middleware = resolve(config.get('wsgi middleware', middleware))
#         args, kwargs = (), {}
#         section = 'wsgi %s' % middleware
#         if config.has_section(section):
#             if config.has_option(section, 'args'):
#                 args = eval(config.get(section, 'args'))
#             if config.has_option(section, 'kwargs'):
#                 kwargs = eval(config.get(section, 'kwargs'))
#         app.wsgi_app = Middleware(app.wsgi_app, *args, **kwargs)

# wsgi.app = app

# import sys
# import subprocess
# debugpy.listen(("0.0.0.0", 51005))
# debugpy.wait_for_client()
# subprocess.run([__file__, *sys.argv[1:]])

with open(__file__) as f:
    exec(compile(f.read(), __file__, 'exec'))
