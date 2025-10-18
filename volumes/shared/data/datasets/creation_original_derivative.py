#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the derivatives/originals of the creations
"""

import random

from proteus import Model

DEPENDS = [
    'release_track',
]


def generate(reclimit=0):

    # constants
    originals_per_remix = reclimit or 2
    foreign_originals_per_remix = reclimit and 1 or 1

    # models
    Creation = Model.get('creation')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])

    # content
    distribution_types = ['original', 'cover', 'adaption', 'remix']

    # create derivative relationships for exisiting creations
    for creation in creations:
        if not creation.release:
            continue
        foreign_creations = Creation.find([
            ('claim_state', '=', 'unclaimed'),
            ('entity_creator', '=', creation.entity_creator),
        ])

        distribution_type = random.choice(distribution_types)
        creation.distribution_type = distribution_type

        other_creations = [
            _creation for _creation in creations
            if _creation.release and _creation.id != creation.id
        ]

        originals = []
        if distribution_type in ['cover', 'adaption']:
            originals = [random.choice(other_creations)]
        elif distribution_type == 'remix':
            originals = random.sample(
                other_creations,
                min(originals_per_remix, len(other_creations)))
            originals += random.sample(
                foreign_creations,
                min(foreign_originals_per_remix, len(foreign_creations)))

        original_ids = [o.id for o in originals]
        originals = Creation.find([('id', 'in', original_ids)])
        creation.original_relations.extend(originals)
        creation.save()
