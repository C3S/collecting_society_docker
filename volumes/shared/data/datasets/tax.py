#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tax and tax codes
"""

from decimal import Decimal

from proteus import Model

DEPENDS = [
    'account_chart',
]


def generate(reclimit=0):

    # models
    Account = Model.get('account.account')
    Tax = Model.get('account.tax')
    TaxCode = Model.get('account.tax.code')

    # entries
    account_tax, = Account.find([
        ('kind', '=', 'other'),
        ('company', '=', 1),
        ('name', '=', 'Main Tax'),
        ])

    # create tax codes
    invoice_base_code = TaxCode(name='invoice base')
    invoice_base_code.save()
    invoice_tax_code = TaxCode(name='invoice tax')
    invoice_tax_code.save()
    credit_note_base_code = TaxCode(name='credit note base')
    credit_note_base_code.save()
    credit_note_tax_code = TaxCode(name='credit note tax')
    credit_note_tax_code.save()

    # create tax
    tax = Tax()
    tax.name = '19% Mehrwertsteuer'
    tax.description = '19% Mehrwertsteuer'
    tax.type = 'percentage'
    tax.rate = Decimal('.19')
    tax.invoice_account = account_tax
    tax.credit_note_account = account_tax
    tax.invoice_base_code = invoice_base_code
    tax.invoice_tax_code = invoice_tax_code
    tax.credit_note_base_code = credit_note_base_code
    tax.credit_note_tax_code = credit_note_tax_code
    tax.save()
