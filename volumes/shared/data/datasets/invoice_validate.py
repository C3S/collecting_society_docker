#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Validate the invoices
"""

from proteus import Model

DEPENDS = [
    'utilisation_allocation_collect',
]


def generate(reclimit=0):

    # model
    Invoice = Model.get('account.invoice')

    # entries
    invoices = Invoice.find([
        ('state', '=', 'draft'),
        ('OR', [
            ('allocation.utilisations.context.name', 'not like', '%invoiced%',
             'event')
        ])
    ])

    # run collections
    for invoice in invoices:
        invoice.click('validate_invoice')
