#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the audio and sheet content
"""

import uuid
import random

from proteus import Model

DEPENDS = [
    'release_track',
    'harddisk_filesystem_label',
]


def generate(reclimit=0):

    # constants
    audio_content_chance_per_creation = reclimit and 1 or 0.8
    content_audio_length_min = reclimit and 60*3 or 30
    content_audio_length_max = reclimit and 60*3 or 60*10
    sheet_content_chance_per_creation = reclimit and 1 or 0.1

    # models
    Creation = Model.get('creation')
    Content = Model.get('content')
    FilesystemLabel = Model.get('harddisk.filesystem.label')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    filesystem_labels = FilesystemLabel.find([])

    # create audio files
    audio_number = 1
    for creation in creations:
        if random.random() > audio_content_chance_per_creation:
            continue
        artist = creation.artist
        if artist.group:
            artist = artist.solo_artists[0]

        # content
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

    # create sheet PDFs
    sheet_number = 1
    for creation in creations:
        if random.random() > sheet_content_chance_per_creation:
            continue
        artist = creation.artist
        if artist.group:
            artist = artist.solo_artists[0]

        # content
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
