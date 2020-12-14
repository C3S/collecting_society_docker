#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create archiving
"""

from proteus import Model

import uuid

DEPENDS = [
    'master'
]


def generate(reclimit):

    # constants
    storehouses = reclimit or 2
    harddisklabels_per_storehouse = reclimit or 2
    harddisks_per_harddisklabel = reclimit or 2
    filesystemlabels_per_harddisk = reclimit or 2
    filesystems_per_filesystemlabel = reclimit or 2

    # models
    Filesystem = Model.get('harddisk.filesystem')
    FilesystemLabel = Model.get('harddisk.filesystem.label')
    Harddisk = Model.get('harddisk')
    HarddiskLabel = Model.get('harddisk.label')
    Storehouse = Model.get('storehouse')
    User = Model.get('res.user')

    for i in range(1, storehouses + 1):
        number = i
        host = uuid_host=str(uuid.uuid4())
        # admin
        admin = User(
            name="Storehouse Admin %s" % str(number).zfill(3),
            login="storehouse%s" % str(number).zfill(3),
            password="%s" % number
        )
        admin.save()
        # storehouse
        storehouse = Storehouse(
            code="%s" % str(number).zfill(3),
            details="Storehouse in City %s" % str(number).zfill(3),
            user=admin
        )
        storehouse.save()
        # harddisk labels
        for j in range(1, harddisklabels_per_storehouse + 1):
            harddisk_label = HarddiskLabel()
            harddisk_label.save()
            # harddisks
            for k in range(1, harddisks_per_harddisklabel + 1):
                harddisk = Harddisk(
                    label=harddisk_label,
                    version=1,
                    storehouse=storehouse,
                    location='SomeMachine',
                    closed=False,
                    raid_type="1",
                    raid_number=str(k),
                    raid_total=str(harddisks_per_harddisklabel),
                    uuid_host=host,
                    uuid_harddisk=str(uuid.uuid4()),
                    user=admin,
                    online=True,
                    state='in_use'
                )
                harddisk.save()
                # filesystem labels
                for l in range(1, filesystemlabels_per_harddisk + 1):
                    filesystem_label = FilesystemLabel()
                    filesystem_label.save()
                    # filesystems
                    for m in range(1, filesystems_per_filesystemlabel + 1):
                        filesystem = Filesystem(
                            label=filesystem_label,
                            harddisk=harddisk,
                            closed=False,
                            partition_number=m,
                            uuid_partition=str(uuid.uuid4()),
                            uuid_raid=str(uuid.uuid4()),
                            uuid_raid_sub=str(uuid.uuid4()),
                            uuid_crypto=str(uuid.uuid4()),
                            uuid_lvm=str(uuid.uuid4()),
                            uuid_filesystem=str(uuid.uuid4())
                        )
                        filesystem.save()