#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create distribution plans
"""

from proteus import  Model

import csv
import datetime

DEPENDS = [
    'master'
]


def generate(reclimit):
    distribution_plans = reclimit or 3
    today = datetime.date.today()
    DistributionPlan = Model.get('distribution.plan')
    for i in range(1, distribution_plans + 1):
        number = i
        DistributionPlan(
            version="%s.0" % number,
            valid_from=today
        ).save()