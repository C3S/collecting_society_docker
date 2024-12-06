#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Posts the invoices
"""

from proteus import Model

DEPENDS = [
    'invoice_validate',
]


def generate(reclimit=0):

    # model
    Invoice = Model.get('account.invoice')

    # entries
    invoices = Invoice.find([
        ('state', '=', 'validated'),
    ])

    # run collections
    for invoice in invoices:
        invoice.click('post')
