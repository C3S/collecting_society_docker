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

    # location categories
    with open(test_location_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            LocationCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()

    # location space categories
    with open(test_location_space_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            LocationSpaceCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()

    # website categories
    with open(test_website_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            WebsiteCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()

    # website resource categories
    with open(test_website_resource_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            wcs = []
            for wc in category['website_categories'].split(","):
                wcs += WebsiteCategory.find(['code', '=', wc])
            WebsiteResourceCategory(
                name=category['name'],
                code=category['code'],
                description=category['description'],
                website_categories=wcs
            ).save()
