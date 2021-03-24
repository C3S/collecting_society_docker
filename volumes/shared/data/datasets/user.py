#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Configure the admin user (German language, company)
"""

from proteus import Model

DEPENDS = [
    'company_employee',
    'language',
]


def generate(reclimit=0):

    # models
    Language = Model.get('ir.lang')
    Company = Model.get('company.company')
    Employee = Model.get('company.employee')
    User = Model.get('res.user')

    # entries
    german_language, = Language.find([('code', '=', 'de_DE')])
    company = Company(1)
    employee = Employee(1)
    user, = User.find([('login', '=', 'admin')])

    # configure user
    user.language = german_language
    user.company = company
    user.employees.extend([employee])
    user.employee = employee
    user.save()
