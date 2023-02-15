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
    originals_per_creation = reclimit or 2
    foreign_originals_per_creation = reclimit and 1 or 1

    # models
    Creation = Model.get('creation')
    Derivative = Model.get('creation.original.derivative')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    foreign_creations = Creation.find([
        ('claim_state', '=', 'unclaimed')])

    # content
    allocation_types = Derivative._fields['allocation_type']['selection']
    allocation_types = [k for k, _ in allocation_types if k]

    # create derivative relationships for exisiting creations
    for creation in creations:
        if not creation.release:
            continue
        others = []
        for other in creations:
            if not other.release or other.id == creation.id:
                continue
            others.append(other)
        originals = random.sample(others, min(
            originals_per_creation, len(others)))
        for original in originals:
            cor = creation.original_relations.new()
            cor.original_creation = original
            cor.derivative_creation = creation
            cor.allocation_type = random.choice(allocation_types)

    # create foreign originals
    for creation in creations:
        for i in range(foreign_originals_per_creation):
            cor = creation.original_relations.new()
            cor.original_creation = random.choice(foreign_creations)
            cor.derivative_creation = creation
            cor.allocation_type = random.choice(allocation_types)

    for creation in creations:
        creation.save()
