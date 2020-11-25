#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create tax and tax codes
"""

from decimal import Decimal
from proteus import Model

DEPENDS = [
    'account_chart'
]


def generate():
    # get account
    Account = Model.get('account.account')
    account_tax, = Account.find([
        ('kind', '=', 'other'),
        ('company', '=', 1),
        ('name', '=', 'Main Tax'),
        ])

    # create tax
    Tax = Model.get('account.tax')
    tax = Tax()
    tax.name = '19% Mehrwertsteuer'
    tax.description = '19% Mehrwertsteuer'
    tax.type = 'percentage'
    tax.rate = Decimal('.19')
    tax.invoice_account = account_tax
    tax.credit_note_account = account_tax

    # create and assign tax codes
    TaxCode = Model.get('account.tax.code')

    invoice_base_code = TaxCode(name='invoice base')
    invoice_base_code.save()
    tax.invoice_base_code = invoice_base_code

    invoice_tax_code = TaxCode(name='invoice tax')
    invoice_tax_code.save()
    tax.invoice_tax_code = invoice_tax_code

    credit_note_base_code = TaxCode(name='credit note base')
    credit_note_base_code.save()
    tax.credit_note_base_code = credit_note_base_code

    credit_note_tax_code = TaxCode(name='credit note tax')
    credit_note_tax_code.save()
    tax.credit_note_tax_code = credit_note_tax_code

    # save tax
    tax.save()
