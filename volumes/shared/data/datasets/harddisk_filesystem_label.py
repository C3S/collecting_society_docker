#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the filesystem labels
"""

from proteus import Model

DEPENDS = [
    'harddisk',
]


def generate(reclimit=0):

    # constants
    filesystemlabels_per_harddisk = reclimit or 2

    # models
    Harddisk = Model.get('harddisk')
    FilesystemLabel = Model.get('harddisk.filesystem.label')

    # entries
    harddisks = Harddisk.find([])

    # create filesystem labels
    for i in range(1, len(harddisks) * filesystemlabels_per_harddisk + 1):
        filesystem_label = FilesystemLabel()
        filesystem_label.save()
