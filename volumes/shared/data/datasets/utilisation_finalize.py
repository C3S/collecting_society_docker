#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Calculate the utilization indicators
"""

from proteus import Model, Wizard

DEPENDS = [
    'utilisation_confirm',
    'artist_playlist_item',
]


def generate(reclimit=0):

    # model
    Utilisation = Model.get('utilisation')
    Warning = Model.get('res.user.warning')

    # prepare dataset we depend upon
    utilisations = Utilisation.find([])

    # recalculate utilisation indicators
    for utilisation in utilisations:
        if utilisation.tariff.category.code == 'L':
            if 'estimated' in utilisation.context.name:
                continue
            if 'confirmed' in utilisation.context.name:
                continue
            warning = Warning(
                user=1,
                name='utilisationgraceperiod,%s' % utilisation.id
            )
            warning.save()
            Wizard('utilisation.finalize', models=[utilisation])
        elif utilisation.tariff.category.code == 'C':
            pass
        elif utilisation.tariff.category.code == 'P':
            pass
        elif utilisation.tariff.category.code == 'O':
            pass
