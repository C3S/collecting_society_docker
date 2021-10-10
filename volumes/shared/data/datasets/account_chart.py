#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the account chart for financial bookkeeping
"""

from proteus import Model, Wizard

DEPENDS = [
    'company',
]


def generate(reclimit=0):

    # models
    Company = Model.get('company.company')
    Account = Model.get('account.account')
    AccountTemplate = Model.get('account.account.template')

    # wizards
    create_chart = Wizard('account.create_chart')

    # entries
    company = Company(1)
    account_template, = AccountTemplate.find([(
        'name', '=', "Kontenplan SKR03 (Germany)")], limit=1)

    # create chart
    create_chart.execute('account')
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute('create_account')

    # get accounts
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

    # assign accounts to chart
    create_chart.form.account_receivable = receivable
    create_chart.form.account_payable = payable

    # create chart properties
    create_chart.execute('create_properties')
