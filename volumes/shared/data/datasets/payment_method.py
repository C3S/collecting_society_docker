#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a payment term
"""

from proteus import Model

DEPENDS = [
    'account_chart',
]


def generate(reclimit=0):

    # models
    PaymentMethod = Model.get('account.invoice.payment.method')
    Company = Model.get('company.company')
    AccountJournal = Model.get('account.journal')
    Account = Model.get('account.account')

    # entries
    company, = Company.find([('party.name', '=', 'C3S SCE')])
    journal, = AccountJournal.find(['code', '=', 'CASH'])
    account, = Account.find(['code', '=', '1200'])

    # create payment term
    payment_method = PaymentMethod(name='Term')
    payment_method.company = company
    payment_method.name = 'Bank'
    payment_method.journal = journal
    payment_method.credit_account = account
    payment_method.debit_account = account
    payment_method.save()
