#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the fiscal year, sequences and period
"""

import datetime
from dateutil.relativedelta import relativedelta

from proteus import Model

DEPENDS = [
    'company',
]


def generate(reclimit=0):

    # models
    Company = Model.get('company.company')
    FiscalYear = Model.get('account.fiscalyear')
    Sequence = Model.get('ir.sequence')
    SequenceType = Model.get('ir.sequence.type')
    SequenceStrict = Model.get('ir.sequence.strict')

    # entries
    company = Company(1)
    sequence_type_account_move, = SequenceType.find(
        [('name', '=', "Buchungssatz")], limit=1)
    sequence_type_invoice, = SequenceType.find(
        [('name', '=', "Rechnung")], limit=1)

    # content
    today = datetime.date.today()

    # create fiscal year
    fiscalyear = FiscalYear(name=str(today.year))
    fiscalyear.start_date = today + relativedelta(month=1, day=1)
    fiscalyear.end_date = today + relativedelta(month=12, day=31)
    fiscalyear.company = company

    # create post move sequence
    pm_sequence = Sequence(
        name=fiscalyear.name, sequence_type=sequence_type_account_move,
        company=company)
    pm_sequence.save()
    fiscalyear.post_move_sequence = pm_sequence

    # create invoice sequence
    iv_sequence = SequenceStrict(
        name=fiscalyear.name, sequence_type=sequence_type_invoice)
    iv_sequence.company = fiscalyear.company
    iv_sequence.save()
    for seq in fiscalyear.invoice_sequences:
        fiscalyear.invoice_sequences.remove(seq)
    invoice_sequence = fiscalyear.invoice_sequences.new()
    invoice_sequence.in_invoice_sequence = iv_sequence
    invoice_sequence.in_credit_note_sequence = iv_sequence
    invoice_sequence.out_invoice_sequence = iv_sequence
    invoice_sequence.out_credit_note_sequence = iv_sequence

    # save fiscal year
    fiscalyear.save()

    # create period
    fiscalyear.click('create_period')
