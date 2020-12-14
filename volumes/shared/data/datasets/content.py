#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create content
"""

from proteus import Model

import uuid

DEPENDS = [
    'creation',
    'archiving'
]


def generate(reclimit):

    # models
    Creation = Model.get('creation')
    FilesystemLabel = Model.get('harddisk.filesystem.label')

    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    filesystem_labels = FilesystemLabel.find([])

    # audio files
    audio_number = 1
    for i in range(1, len(creations) + 1):
        if random.random() > audio_content_chance_per_creation:
            continue
        creation = creations[i - 1]
        artist = creation.artist
        if artist.group:
            artist = artist.solo_artists[0]

        # audio
        c = Content()
        c.uuid = str(uuid.uuid4())
        c.commit_state = 'commited'
        c.entity_creator = artist.party
        c.category = 'audio'
        c.creation = creation
        # file metadata
        c.name = "audio_%s.wav" % str(audio_number).zfill(3)
        c.size = 12345
        c.mime_type = 'audio/x-wav'
        # file processing
        c.path = '/some/path'
        c.preview_path = '/some/preview/path'
        c.filesystem_label = random.choice(filesystem_labels)
        c.processing_state = 'archived'
        c.storage_hostname = 'archive_machine'
        c.mediation = False
        # low level audio metadata
        c.length = round(random.uniform(
            content_audio_length_min, content_audio_length_max), 6)
        c.channels = 2
        c.sample_rate = 48000
        c.sample_width = 16
        # high level metadata
        c.metadata_artist = creation.artist.name
        c.metadata_title = creation.title
        c.metadata_release = creation.release.title
        c.metadata_release_date = str(creation.release.release_date)
        c.metadata_track_number = "0"
        c.save()
        audio_number += 1

    # sheet PDFs

    sheet_number = 1
    for i in range(1, len(creations) + 1):
        if random.random() > sheet_content_chance_per_creation:
            continue
        creation = creations[i - 1]
        artist = creation.artist
        if artist.group:
            artist = artist.solo_artists[0]

        c = Content()
        c.uuid = str(uuid.uuid4())
        c.entity_creator = artist.party
        c.category = 'sheet'
        c.creation = creation
        # file metadata
        c.name = "sheet_%s.pdf" % str(sheet_number).zfill(3)
        c.size = 54321
        c.mime_type = 'application/pdf'
        # file processing
        c.path = '/some/path'
        c.filesystem_label = random.choice(filesystem_labels)
        c.processing_state = 'archived'
        c.storage_hostname = 'archive_machine'
        c.mediation = False
        c.save()
        sheet_number += 1
