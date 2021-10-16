#!/usr/bin/env python
# EASY-INSTALL-DEV-SCRIPT: 'trytond==3.4.19','trytond'

import socket
import ptvsd
from trytond import wsgi

__requires__ = 'trytond'
__import__('pkg_resources').require('trytond')
__file__ = '/shared/src/trytond/bin/trytond'


class PtvsdTrytondWSGI(wsgi.TrytondWSGI):
    def __init__(self, *args, **kwargs):
        try:
            print("enabling debugger")
            ptvsd.enable_attach(address=("0.0.0.0", 51005))
        except socket.error:
            print("debugger socket already taken")
        super().__init__(*args, **kwargs)


wsgi.app = PtvsdTrytondWSGI()

with open(__file__) as f:

    # try:
    #     ptvsd.enable_attach(address=("0.0.0.0", 51005), redirect_output=True)
    # except socket.error:
    #     print("socket error while attaching to ptvsd. (If this is a "
    #           "restart and the port is already open, you can ignore this "
    #           "message.)")
    # ptvsd.wait_for_attach();
    # ptvsd.break_into_debugger()
    # content = f.read()
    # content = """
    # from trytond import wsgi
    # print(wsgi.app.__class__.__name__)
    # """ + content

    exec(compile(f.read(), __file__, 'exec'))
