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
    'creation',
]


def generate(reclimit=0):

    # constants
    originals_per_remix = reclimit or 2
    foreign_originals_per_remix = reclimit and 1 or 1

    # models
    Creation = Model.get('creation')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    foreign_creations = Creation.find([('claim_state', '=', 'unclaimed')])

    # content
    allocation_types = ['cover', 'adaption', 'remix', None]

    # create derivative relationships for exisiting creations
    for creation in creations:
        if not creation.release:
            continue

        allocation_type = random.choice(allocation_types)
        if not allocation_type:
            continue

        others = []
        for other in creations:
            if not other.release or other.id == creation.id:
                continue
            others.append(other)

        if allocation_type in ['cover', 'adaption']:
            originals = [random.choice(others)]
        elif allocation_type == 'remix':
            originals = random.sample(
                others,
                min(originals_per_remix, len(others)))
            originals += random.sample(
                foreign_creations,
                min(foreign_originals_per_remix, len(foreign_creations)))

        for original in originals:
            cor = creation.original_relations.new()
            cor.original_creation = original
            cor.derivative_creation = creation
            cor.allocation_type = allocation_type

    for creation in creations:
        creation.save()
