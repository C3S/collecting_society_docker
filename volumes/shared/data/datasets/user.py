#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Configure admin user (German language, company)
"""

from proteus import Model

DEPENDS = [
    'company',
    'language',
]


def generate():
    # get language
    Language = Model.get('ir.lang')
    german_language, = Language.find([('code', '=', 'de_DE')])

    # get company
    Company = Model.get('company.company')
    company = Company(1)

    # configure user
    User = Model.get('res.user')
    user, = User.find([('login', '=', 'admin')])
    user.language = german_language
    user.company = company
    user.save()
