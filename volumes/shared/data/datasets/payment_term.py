#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a payment term
"""

from proteus import Model

DEPENDS = [
    'upgrade'
]


def generate():
    PaymentTerm = Model.get('account.invoice.payment_term')
    PaymentTermLine = Model.get('account.invoice.payment_term.line')
    payment_term = PaymentTerm(name='Term')
    payment_term_line = PaymentTermLine(type='remainder', days=14)
    payment_term.lines.append(payment_term_line)
    payment_term.save()
