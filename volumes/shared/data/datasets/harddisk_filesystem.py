#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the filesystems
"""

import uuid
from itertools import cycle

from proteus import Model

DEPENDS = [
    'harddisk_filesystem_label',
]


def generate(reclimit=0):

    # constants
    filesystems_per_filesystemlabel = reclimit or 2

    # models
    Filesystem = Model.get('harddisk.filesystem')
    FilesystemLabel = Model.get('harddisk.filesystem.label')
    Harddisk = Model.get('harddisk')

    # entries
    harddisks = Harddisk.find([])
    filesystem_labels = FilesystemLabel.find([])

    # create filesystems
    for harddisk, filesystem_label in zip(cycle(harddisks), filesystem_labels):
        for i in range(1, filesystems_per_filesystemlabel + 1):
            filesystem = Filesystem(
                label=filesystem_label,
                harddisk=harddisk,
                closed=False,
                partition_number=i,
                uuid_partition=str(uuid.uuid4()),
                uuid_raid=str(uuid.uuid4()),
                uuid_raid_sub=str(uuid.uuid4()),
                uuid_crypto=str(uuid.uuid4()),
                uuid_lvm=str(uuid.uuid4()),
                uuid_filesystem=str(uuid.uuid4())
            )
            filesystem.save()
