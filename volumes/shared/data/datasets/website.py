#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the websites
"""

from proteus import Model

DEPENDS = [
    'web_user',
    'website_category',
]


def generate(reclimit=0):

    # constants
    radio_websites_per_licensee = reclimit or 1

    # models
    WebUser = Model.get('web.user')
    Website = Model.get('website')
    WebsiteCategory = Model.get('website.category')

    # entries
    licensees = WebUser.find([('roles.code', '=', 'licensee')])
    website_category_webradio, = WebsiteCategory.find([('code', '=', 'R')])

    # create websites for webradio
    for i, licensee in enumerate(licensees):
        for j in range(1, radio_websites_per_licensee + 1):
            number = i * radio_websites_per_licensee + j
            Website(
                name='Webradio %s' % str(number).zfill(3),
                category=website_category_webradio,
                party=licensee.party,
                url='https://webradio%s.test' % str(number).zfill(3)
            ).save()
