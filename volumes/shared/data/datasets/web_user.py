#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create web users
"""

from proteus import  Model

import datetime
import random

DEPENDS = [
    'master'
]


def generate(reclimit):

    # constants
    group_artists = reclimit or 3
    new_solo_artists_per_group = reclimit or 2
    add_solo_artists_per_group = reclimit or 1
    foreign_artists_per_group = reclimit or 1
    webuser_licensee = reclimit or 3
    webuser_all_roles = reclimit or 2

    # models
    WebUser = Model.get('web.user')
    WebUserRole = Model.get('web.user.role')

    # Role: Licenser
    i = 0
    for i in range(1, group_artists * new_solo_artists_per_group + 1):
        number = i
        total = i
        birthdate = datetime.date(
            random.randint(1950, 2000),
            random.randint(1, 12),
            random.randint(1, 28))
        firstname = "Registered Name"
        lastname = "%s" % str(total).zfill(3)
        web_user = WebUser(
            email='licenser%s@collecting-society.test' % number,
            nickname=firstname + ' ' + lastname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([('code', '=', 'licenser')])
        web_user.roles.extend(roles)
        web_user.default_role = 'licenser'
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = firstname + ' ' + lastname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.save()

    # Role: Licensee
    for j in range(1, webuser_licensee + 1):
        number = j
        total = i + j
        birthdate = datetime.date(
            random.randint(1950, 2000),
            random.randint(1, 12),
            random.randint(1, 28))
        firstname = "Registered Name"
        lastname = "%s" % str(total).zfill(3)
        web_user = WebUser(
            email='licensee%s@collecting-society.test' % number,
            nickname=firstname + ' ' + lastname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([('code', '=', 'licensee')])
        web_user.roles.extend(roles)
        web_user.default_role = 'licensee'
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = firstname + ' ' + lastname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.save()

    # Role: All
    for k in range(1, webuser_all_roles + 1):
        number = k
        total = i + j + k
        birthdate = datetime.date(
            random.randint(1950, 2000),
            random.randint(1, 12),
            random.randint(1, 28))
        firstname = "Registered Name"
        lastname = "%s" % str(total).zfill(3)
        web_user = WebUser(
            email='allroles%s@collecting-society.test' % number,
            nickname=firstname + ' ' + lastname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([
            'OR',
            ('code', '=', 'licenser'),
            ('code', '=', 'licensee')])
        web_user.roles.extend(roles)
        web_user.default_role = roles[k - 1 % len(roles)].code
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = firstname + ' ' + lastname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.save()