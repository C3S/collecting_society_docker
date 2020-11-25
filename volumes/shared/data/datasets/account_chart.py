#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a chart of the accounts
"""

from proteus import Model, Wizard

DEPENDS = [
    'company'
]


def generate():
    # get company
    Company = Model.get('company.company')
    company = Company(1)

    # get account template
    AccountTemplate = Model.get('account.account.template')
    account_template, = AccountTemplate.find([('parent', '=', None)])

    # create chart
    create_chart = Wizard('account.create_chart')
    create_chart.execute('account')
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute('create_account')

    # get accounts
    Account = Model.get('account.account')
    receivable, = Account.find([
        ('kind', '=', 'receivable'),
        ('company', '=', company.id),
        ])
    payable, = Account.find([
        ('kind', '=', 'payable'),
        ('company', '=', company.id),
        ])

    # assign accounts to chart
    create_chart.form.account_receivable = receivable
    create_chart.form.account_payable = payable

    # create chart properties
    create_chart.execute('create_properties')
