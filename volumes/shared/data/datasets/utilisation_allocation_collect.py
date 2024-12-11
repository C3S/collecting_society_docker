#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Run the collections
"""

import math
from proteus import Model, Wizard

DEPENDS = [
    'utilisation_finalize',
]

# constants
repeats_per_distribution_received = 3


def generate(reclimit=0):

    # model
    Utilisation = Model.get('utilisation')
    PaymentMethod = Model.get('account.invoice.payment.method')

    # entries
    payment_method, = PaymentMethod.find()
    utilisations_invoiced = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%invoiced%', 'event'),
        ])
    ])
    utilisations_posted = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%posted%', 'event'),
        ])
    ])
    utilisations_paid = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%paid%', 'event'),
        ])
    ])
    utilisations_distributed = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%distributed%', 'event'),
        ])
    ])
    utilisations_received = Utilisation.find([
        ('state', '=', 'finalized'),
        ('OR', [
            # live
            ('context.name', 'like', '%received%', 'event'),
        ])
    ])

    # run collections
    for batch in [utilisations_invoiced,
                  utilisations_posted,
                  utilisations_paid,
                  utilisations_distributed]:
        wizard = Wizard('utilisation.allocation.collect', models=batch)
        wizard.execute('collect')

    # run collections for received distributions
    batch_size = repeats_per_distribution_received
    length = len(utilisations_received)
    batches = math.ceil(length / batch_size)
    for i in range(0, batches):
        start = i * batch_size
        end = min(start + batch_size, length)
        batch = utilisations_received[start:end]

        wizard = Wizard('utilisation.allocation.collect', models=batch)
        wizard.execute('collect')

    # invoice state posted
    for batch in [utilisations_posted,
                  utilisations_paid,
                  utilisations_distributed,
                  utilisations_received]:
        invoices = set([
            utilisation.allocation.invoice
            for utilisation in batch
        ])
        for invoice in invoices:
            invoice.click('validate_invoice')
            invoice.click('post')

    # invoice state paid
    for batch in [utilisations_paid,
                  utilisations_distributed,
                  utilisations_received]:
        invoices = set([
            utilisation.allocation.invoice
            for utilisation in batch
        ])
        for invoice in invoices:
            pay = invoice.click('pay')
            pay.form.payment_method = payment_method
            pay.execute('choice')
