#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create transitory journal
"""

from proteus import Model

DEPENDS = [
    'company',
]


def generate():
    # get sequence
    Sequence = Model.get('ir.sequence')
    sequence, = Sequence.find([('code', '=', 'account.journal')])

    # create journal
    AccountJournal = Model.get('account.journal')
    journal = AccountJournal(
        name='Transitory', code='TRANS', type='general', sequence=sequence)
    journal.save()
