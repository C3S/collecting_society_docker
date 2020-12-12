#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create derivatives
"""

from proteus import  Model

import random

DEPENDS = [
    'creation'
]


def generate(reclimit):

    # constants
    originals_per_creation = reclimit or 2
    foreign_originals_per_creation = reclimit and 1 or 1

    # content
    allocation_types = [
        'adaption',
        'cover',
        'remix',
    ]

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')

    creations = Creation.find([('claim_state', '!=', 'unclaimed')])

    # Exisiting creations::

    for i in range(0, len(creations)):
        creation = creations[i]
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
            cor.save()
            creation.save()
    # Foreign originals
    for i in range(0, len(creations)):
        creation = creations[i]
        for j in range(1, foreign_originals_per_creation + 1):
            number = i * foreign_originals_per_creation + j
            foreign_artist = Artist(
                name="Foreign Original Artist %s" % str(number).zfill(3),
                group=False,
                entity_creator=creation.entity_creator,
                entity_origin='indirect',
                commit_state='uncommited',
                claim_state='unclaimed'
            )
            foreign_artist.save()
            foreign_original = Creation(
                title="Foreign Original Song %s" % str(number).zfill(3),
                artist=foreign_artist,
                entity_creator=creation.entity_creator,
                entity_origin='indirect',
                commit_state='uncommited',
                claim_state='unclaimed'
            )
            foreign_original.save()

            cor = creation.original_relations.new()
            cor.original_creation = foreign_original
            cor.derivative_creation = creation
            cor.allocation_type = random.choice(allocation_types)
            cor.save()
            creation.save()
