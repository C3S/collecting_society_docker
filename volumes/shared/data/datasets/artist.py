#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the solo/group/foreign artists
"""

import random

from proteus import Model

from . import test_text

DEPENDS = [
    'web_user',
]


def generate(reclimit=0):

    # constants
    group_artists = reclimit or 3
    new_solo_artists_per_group = reclimit or 2
    add_solo_artists_per_group = reclimit or 1
    foreign_artists_per_group = reclimit or 1
    foreign_artists_for_originals = reclimit or 10

    # models
    WebUser = Model.get('web.user')
    Artist = Model.get('artist')
    Party = Model.get('party.party')

    # entries
    web_users = WebUser.find([('roles.code', '=', 'licensee')])

    # create artists
    for i in range(1, group_artists + 1):
        number = i
        web_user_number = (number - 1) * new_solo_artists_per_group + 1
        web_user, = WebUser.find([(
            'nickname', '=', 'Registered Name %s' % str(
                web_user_number).zfill(3)
        )])

        # group artists
        group_artist = Artist(
            name="Group Artist %s" % str(number).zfill(3),
            group=True,
            entity_creator=web_user.party,
            entity_origin='direct',
            commit_state='commited',
            claim_state='claimed',
            description=test_text
        )

        # members
        for j in range(1, new_solo_artists_per_group + 1):
            number = (i - 1) * new_solo_artists_per_group + j
            web_user, = WebUser.find([(
                'nickname', '=', 'Registered Name %s' % str(
                    number).zfill(3)
            )])
            group_artist.solo_artists.new(
                name="Solo Artist %s" % str(number).zfill(3),
                group=False,
                party=web_user.party,
                entity_creator=web_user.party,
                entity_origin='direct',
                commit_state='commited',
                claim_state='claimed',
                description=test_text
            )

        # foreign members
        for k in range(1, foreign_artists_per_group + 1):
            number = (i - 1) * foreign_artists_per_group + k
            name = "Foreign Member Solo Artist %s" % str(number).zfill(3)
            foreign_solo_artist_party = Party(
                name=name
            )
            _ = foreign_solo_artist_party.contact_mechanisms.new(
                type='email',
                value="foreign_member_%s@rep.test" % number
            )
            foreign_solo_artist_party.save()
            group_artist.solo_artists.new(
                name=name,
                group=False,
                party=foreign_solo_artist_party,
                entity_creator=web_user.party,
                entity_origin='indirect',
                commit_state='uncommited',
                claim_state='unclaimed'
            )

        # save
        group_artist.save()

    # add existing solo artists to group artists
    groups = Artist.find([
        ('claim_state', '!=', 'unclaimed'),
        ('group', '=', True)])
    for i, group in enumerate(groups):
        solos = Artist.find([
            ('claim_state', '!=', 'unclaimed'),
            ('group', '=', False)])
        for j in range(0, add_solo_artists_per_group):
            if solos <= group.solo_artists:
                continue
            solo = random.choice(solos)
            while solo in group.solo_artists:
                solo = random.choice(solos)
            group.solo_artists.extend([solo])
            group.save()

    # create foreign artists for originals
    for i in range(1, foreign_artists_for_originals + 1):
        web_user = random.choice(web_users)
        Artist(
            name="Foreign Original Artist %s" % str(i).zfill(3),
            group=False,
            entity_creator=web_user.party,
            entity_origin='indirect',
            commit_state='uncommited',
            claim_state='unclaimed'
        ).save()
