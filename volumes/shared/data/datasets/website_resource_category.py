#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the website resource categories
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'website_category',
]


def generate(reclimit=0):

    # models
    WebsiteCategory = Model.get('website.category')
    WebsiteResourceCategory = Model.get('website.resource.category')

    # create website resource categories
    path = os.path.join('data', 'csv', 'website_resource_category.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for i, row in enumerate(reader):
            wcs = []
            for wc in row['website_categories'].split(","):
                wcs += WebsiteCategory.find(['code', '=', wc])
            WebsiteResourceCategory(
                name=row['name'],
                code=row['code'],
                description=row['description'],
                website_categories=wcs
            ).save()
