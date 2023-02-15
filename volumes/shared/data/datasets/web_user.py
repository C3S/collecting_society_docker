#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the web users for licenser/licensee/all roles
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    group_artists = reclimit or 3
    new_solo_artists_per_group = reclimit or 2
    webuser_licensee = reclimit or 1
    webuser_all_roles = reclimit or 1

    # models
    Company = Model.get('company.company')
    Account = Model.get('account.account')
    WebUser = Model.get('web.user')
    WebUserRole = Model.get('web.user.role')

    # entries
    company = Company(1)
    receivable, = Account.find([
            ('type.receivable', '=', True),
            ('party_required', '=', True),
            ('company', '=', company.id),
            ], limit=1)
    payable, = Account.find([
            ('type.payable', '=', True),
            ('party_required', '=', True),
            ('company', '=', company.id),
            ], limit=1)

    # Role: Licenser
    for i in range(1, group_artists * new_solo_artists_per_group + 1):
        number = i
        total = i
        birthdate = datetime.date(
            random.randint(1950, 2000),
            random.randint(1, 12),
            random.randint(1, 28))
        firstname = "Registered Name"
        lastname = "%s" % str(total).zfill(3)
        nickname = "%s %s" % (firstname, lastname)
        web_user = WebUser(
            email='licenser%s@collecting-society.test' % number,
            nickname=nickname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([('code', '=', 'licenser')])
        web_user.roles.extend(roles)
        web_user.default_role = 'licenser'
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = nickname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.account_receivable = receivable
        web_user.party.account_payable = payable
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
        nickname = "%s %s" % (firstname, lastname)
        web_user = WebUser(
            email='licensee%s@collecting-society.test' % number,
            nickname=nickname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([('code', '=', 'licensee')])
        web_user.roles.extend(roles)
        web_user.default_role = 'licensee'
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = nickname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.account_receivable = receivable
        web_user.party.account_payable = payable
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
        nickname = "%s %s" % (firstname, lastname)
        web_user = WebUser(
            email='allroles%s@collecting-society.test' % number,
            nickname=nickname,
            password="password",
            opt_in_state='opted-in'
        )
        roles = WebUserRole.find([])
        web_user.roles.extend(roles)
        web_user.default_role = roles[(k - 1) % len(roles)].code
        web_user.save()
        web_user.party.firstname = firstname
        web_user.party.lastname = lastname
        web_user.party.name = nickname
        web_user.party.repertoire_terms_accepted = True
        web_user.party.birthdate = birthdate
        web_user.party.account_receivable = receivable
        web_user.party.account_payable = payable
        web_user.party.save()
