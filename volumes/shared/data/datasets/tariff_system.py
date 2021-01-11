#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff systems
"""

import datetime

from proteus import Model

DEPENDS = [
    'master',
]


def generate(reclimit=0):

    # constants
    tariff_systems = reclimit and reclimit or 3

    # models
    TariffSystem = Model.get('tariff_system')

    # content
    today = datetime.date.today()

    # create tariff systems
    for i in range(1, tariff_systems + 1):
        TariffSystem(
            version="%s.0" % i,
            valid_from=today
        ).save()
