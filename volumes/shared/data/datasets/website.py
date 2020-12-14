#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create website
"""

from proteus import Model

import csv

DEPENDS = [
    'master'
]


def generate(reclimit):

    #constants
    test_website_categories = '/shared/data/csv/website_categories.csv'
    test_website_resource_categories = '/shared/data/csv/website_resource_categories.csv'
    delimiter = ','
    quotechar = '"'

    # models
    WebsiteCategory = Model.get('website.category')
    WebsiteResourceCategory = Model.get('website.resource.category')

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
