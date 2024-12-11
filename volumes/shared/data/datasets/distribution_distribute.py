#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Run the distributions
"""

import math
from proteus import Model, Wizard

DEPENDS = [
    'utilisation_allocation_collect',
]


def generate(reclimit=0):

    # constants
    allocations_per_distribution = 4

    # model
    Allocation = Model.get('allocation')
    PaymentMethod = Model.get('account.invoice.payment.method')

    # entries
    payment_method, = PaymentMethod.find()
    allocations_distributed = Allocation.find([
        ('state', '=', 'collected'),
        ('OR', [
            # live
            ('utilisations.context.name', 'like', '%distributed%', 'event'),
        ])
    ])
    allocations_received = Allocation.find([
        ('state', '=', 'collected'),
        ('OR', [
            # live
            ('utilisations.context.name', 'like', '%received%', 'event'),
        ])
    ])

    # run distributions
    batch_size = allocations_per_distribution
    for allocations in [allocations_distributed, allocations_received]:
        length = len(allocations)
        batches = math.ceil(length / batch_size)
        for i in range(0, batches):
            start = i * batch_size
            end = min(start + batch_size, length)
            batch = allocations[start:end]

            wizard = Wizard('distribution.distribute', models=batch)
            wizard.execute('distribute')

    # invoice state paid
    for allocation in allocations_received:
        for invoice in allocation.distribution.licenser_invoices:
            pay = invoice.click('pay')
            pay.form.payment_method = payment_method
            pay.execute('choice')
