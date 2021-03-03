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
    episodes_per_podcast_website = reclimit or 3

    # models
    Website = Model.get('website')
    WebsiteResourceCategory = Model.get('website.resource.category')

    # entries
    radio_websites = Website.find(['category.code', '=', 'R'])
    podcast_websites = Website.find(['category.code', '=', 'P'])
    category_channel, = WebsiteResourceCategory.find([('code', '=', 'C')])
    category_episode, = WebsiteResourceCategory.find([('code', '=', 'E')])

    # create websites resources for webradios
    for i, website in enumerate(radio_websites):
        for j in range(1, channels_per_radio_website + 1):
            number = j
            resource = website.resources.new()
            resource.category = category_channel
            resource.name = 'Webradio %s Channel %s' % (
                website.name[-3:],
                str(number).zfill(3)
            )
            resource.url = 'https://channel%s.webradio%s.test' % (
                str(number).zfill(3),
                website.name[-3:]
            )
        website.save()

    # create websites resources for podcasts
    for i, website in enumerate(podcast_websites):
        for j in range(1, episodes_per_podcast_website + 1):
            number = j
            resource = website.resources.new()
            resource.category = category_episode
            resource.name = 'Podcast %s Episode %s' % (
                website.name[-3:],
                str(number).zfill(3),
            )
            resource.url = 'https://podcast%s.test/episode%s' % (
                website.name[-3:],
                str(number).zfill(3)
            )
        website.save()
