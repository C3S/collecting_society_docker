#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a transitory account view
"""

from proteus import Model

DEPENDS = [
    'account_chart'
]


def generate():
    # get company
    Company = Model.get('company.company')
    company = Company(1)

    # get root account
    Account = Model.get('account.account')
    root_account, = Account.find([('name', '=', 'Minimal Account Chart')])

    # create view
    transitory_account_view = Account(
        name='Transitory Accounts',
        kind='view',
        parent=root_account,
        company=company)
    transitory_account_view.save()
