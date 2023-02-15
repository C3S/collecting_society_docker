#!/usr/bin/env python
# EASY-INSTALL-DEV-SCRIPT: 'trytond==3.4.19','trytond'

import ptvsd
import socket

__requires__ = 'trytond'
__import__('pkg_resources').require('trytond')
__file__ = '/shared/src/trytond/bin/trytond'
with open(__file__) as f:

    try:
        ptvsd.enable_attach(address=("0.0.0.0", 51005), redirect_output=True)
    except socket.error:
        pass
    # ptvsd.wait_for_attach(); ptvsd.break_into_debugger()

    exec(compile(f.read(), __file__, 'exec'))
