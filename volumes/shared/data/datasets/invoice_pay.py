#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Pays the invoices
"""

from proteus import Model

DEPENDS = [
    'invoice_post',
]


def generate(reclimit=0):

    # model
    Invoice = Model.get('account.invoice')
    PaymentMethod = Model.get('account.invoice.payment.method')

    # entries
    payment_method, = PaymentMethod.find()
    invoices = Invoice.find([
        ('state', '=', 'posted'),
        ('OR', [
            ('allocation.utilisations.context.name', 'not like', '%posted%',
             'event')
        ])
    ])

    # run collections
    for invoice in invoices:
        pay = invoice.click('pay')
        pay.form.payment_method = payment_method
        pay.execute('choice')
