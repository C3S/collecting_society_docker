#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Run the collections
"""

from proteus import Model, Wizard

DEPENDS = [
    'utilisation_finalize',
]


def generate(reclimit=0):

    # model
    Utilisation = Model.get('utilisation')

    # entries
    utilisations_invoiced = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%invoiced%', 'event'),
        ])
    ])
    utilisations_posted = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%posted%', 'event'),
        ])
    ])
    utilisations_paid = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%paid%', 'event'),
        ])
    ])
    utilisations_distributed = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%distributed%', 'event'),
        ])
    ])

    # run collections
    for batch in [utilisations_invoiced,
                  utilisations_posted,
                  utilisations_paid,
                  utilisations_distributed]:
        wizard = Wizard('utilisation.allocation.collect', models=batch)
        wizard.execute('collect')
