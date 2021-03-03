#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the websites resources
"""

from proteus import Model

DEPENDS = [
    'website_resource_category',
    'website',
]


def generate(reclimit=0):

    # constants
    channels_per_radio_website = reclimit or 3

    # models
    Website = Model.get('website')
    WebsiteResourceCategory = Model.get('website.resource.category')

    # entries
    radio_websites = Website.find(['category.code', '=', 'R'])
    category_channel, = WebsiteResourceCategory.find([('code', '=', 'C')])

    # create websites resources for webradio
    for i, radio_website in enumerate(radio_websites):
        for j in range(1, channels_per_radio_website):
            number = i * channels_per_radio_website + j
            resource = radio_website.resources.new()
            resource.name = 'Webradio Channel %s' % str(number).zfill(3)
            resource.category = category_channel
            resource.url = 'https://channel%s.webradio%s.test' % (
                str(number).zfill(3),
                str(number).zfill(3)
            )
        radio_website.save()
