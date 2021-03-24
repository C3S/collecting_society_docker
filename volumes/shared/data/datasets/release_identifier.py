#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the release identifiers
"""

from proteus import Model

DEPENDS = [
    'creation',
]


def generate(reclimit=0):

    # models
    Release = Model.get('release')
    ReleaseIdentifierSpace = Model.get('release.identifier.space')

    # entries
    releases = Release.find([])
    space_grid, = ReleaseIdentifierSpace.find([('name', '=', 'GRid')])
    space_eanupc, = ReleaseIdentifierSpace.find([('name', '=', 'EAN/UPC')])

    # create release identifiers
    for i, release in enumerate(releases, start=1):

        # grid
        grid = release.identifiers.new()
        grid.space = space_grid
        grid.id_code = "%s-%s-%s-%s" % (
            'A1', 'ABCDE', str(i).zfill(10), 'M'
        )

        # eanupc
        eanupc = release.identifiers.new()
        eanupc.space = space_grid
        eanupc.id_code = "%s" % str(i).zfill(13)

        release.save()
