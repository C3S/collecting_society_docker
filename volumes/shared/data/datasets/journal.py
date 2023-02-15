#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create a transitory journal
"""

from proteus import Model

DEPENDS = [
    'company',
]


def generate(reclimit=0):

    # models
    Sequence = Model.get('ir.sequence')
    AccountJournal = Model.get('account.journal')

    # entries
    sequence, = Sequence.find(
        [('sequence_type.name', '=', "Buchhaltung Journal")], limit=1)

    # create journal
    journal = AccountJournal(
        name='Transitory', code='TRANS', type='general', sequence=sequence)
    journal.save()
