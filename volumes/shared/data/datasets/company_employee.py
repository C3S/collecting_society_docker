#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the company employees
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'account_chart',
]


def generate(reclimit=0):

    # models
    Account = Model.get('account.account')
    Country = Model.get('country.country')
    Company = Model.get('company.company')
    Employee = Model.get('company.employee')
    Party = Model.get('party.party')

    # entries
    company = Company(1)
    receivable, = Account.find([
        ('kind', '=', 'receivable'),
        ('company', '=', company.id),
        ])
    payable, = Account.find([
        ('kind', '=', 'payable'),
        ('company', '=', company.id),
        ])

    # create party (first row of collecting_socity.csv)
    path = os.path.join('data', 'csv', 'collecting_society.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        row = reader.next()
        country, = Country.find([('code', '=', row['country'])])
        party = Party(name="Employee")
        _ = party.addresses.pop()
        party.addresses.new(
            street=row['street'],
            zip=row['zip'],
            city=row['city'],
            country=country
        )
        party.account_receivable = receivable
        party.account_payable = payable
        party.save()

    # create employee
    employee = Employee()
    employee.party = party
    employee.company = company
    employee.save()
