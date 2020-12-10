#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create genres and styles
"""

from proteus import  Model

import random
import csv

DEPENDS = [
    'master'
]


def generate(reclimit):
    test_genres = '/shared/data/csv/genres.csv'
    test_styles = '/shared/data/csv/styles.csv'
    delimiter = ','
    quotechar = '"'

    # get genres
    Genre = Model.get('genre')
    with open(test_genres, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for genre in reader:
            if reclimit and i > reclimit:
                break
            # if label and i > label:  # TODO: check if necessary
            #     break
            i += 1
            Genre(
                name=genre['name'],
                description=genre['description']
            ).save()

    # get styles
    Style = Model.get('style')
    with open(test_styles, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for style in reader:
            if reclimit and i > reclimit:
                break
            i += 1
            Style(
                name=style['name'],
                description=style['description']
            ).save()
