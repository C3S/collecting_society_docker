#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the storehouses and storehouse admins
"""

from proteus import Model

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    storehouses = reclimit or 2

    # models
    User = Model.get('res.user')
    Storehouse = Model.get('storehouse')

    # create storehouses
    for i in range(1, storehouses + 1):
        number = i
        # admin
        admin = User(
            name="Storehouse Admin %s" % str(number).zfill(3),
            login="storehouse%s" % str(number).zfill(3),
            password="password"
        )
        admin.save()
        # storehouse
        storehouse = Storehouse(
            code="%s" % str(number).zfill(3),
            details="Storehouse in City %s" % str(number).zfill(3),
            user=admin
        )
        storehouse.save()
