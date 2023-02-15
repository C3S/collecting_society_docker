#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a transitory account view
"""

from proteus import Model

DEPENDS = [
    'account_chart',
]


def generate(reclimit=0):

    # models
    Company = Model.get('company.company')
    Account = Model.get('account.account')
    AccountType = Model.get('account.account.type')

    # entries
    company = Company(1)
    root_account, = Account.find(
        [('name', '=', "Kontenplan SKR03 (Germany)")], limit=1)
    # account_type_view, = AccountType.find([('name', '=', 'View')], limit=1)

    # create view
    # transitory_account_view = Account(
    #     name='Transitory Accounts',
    #     type=account_type_view,
    #     parent=root_account,
    #     company=company)
    # transitory_account_view.save()
