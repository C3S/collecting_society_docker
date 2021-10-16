#!/usr/bin/env python
# EASY-INSTALL-DEV-SCRIPT: 'trytond==3.4.19','trytond'

import socket
import debugpy
from trytond import wsgi

__requires__ = 'trytond'
__import__('pkg_resources').require('trytond')
__file__ = '/shared/src/trytond/bin/trytond'


class DebugpyTrytondWSGI(wsgi.TrytondWSGI):
    def __init__(self, *args, **kwargs):
        try:
            print("enabling debugger")
            debugpy.listen(("0.0.0.0", 51005))
        except socket.error:
            print("debugger socket already taken")
        super().__init__(*args, **kwargs)


wsgi.app = DebugpyTrytondWSGI()

with open(__file__) as f:
    exec(compile(f.read(), __file__, 'exec'))
