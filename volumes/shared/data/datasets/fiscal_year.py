#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the fiscal year, sequences and period
"""

import datetime
from dateutil.relativedelta import relativedelta

from proteus import config, Model

DEPENDS = [
    'company',
]


def generate(reclimit=0):

    # models
    Company = Model.get('company.company')
    FiscalYear = Model.get('account.fiscalyear')
    Sequence = Model.get('ir.sequence')
    SequenceStrict = Model.get('ir.sequence.strict')

    # entries
    company = Company(1)
    context = config.get_config()._context

    # content
    today = datetime.date.today()

    # create fiscal year
    fiscal_year = FiscalYear(name='%s' % today.year)
    fiscal_year.start_date = today + relativedelta(month=1, day=1)
    fiscal_year.end_date = today + relativedelta(month=12, day=31)
    fiscal_year.company = company

    # create sequence
    post_move_sequence = Sequence(
        name='%s' % today.year, code='account.move', company=company)
    post_move_sequence.save()
    fiscal_year.post_move_sequence = post_move_sequence
    invoice_seq = SequenceStrict(
        name=str(today.year), code='account.invoice', company=company)
    invoice_seq.save()

    # assign sequence
    fiscal_year.out_invoice_sequence = invoice_seq
    fiscal_year.in_invoice_sequence = invoice_seq
    fiscal_year.out_credit_note_sequence = invoice_seq
    fiscal_year.in_credit_note_sequence = invoice_seq

    # save fiscal year
    fiscal_year.save()

    # create period
    FiscalYear.create_period([fiscal_year.id], context)
