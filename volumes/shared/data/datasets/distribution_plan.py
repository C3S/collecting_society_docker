#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the distribution plans
"""

import datetime

from proteus import Model

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    distribution_plans = reclimit or 3

    # models
    DistributionPlan = Model.get('distribution.plan')

    # content
    today = datetime.date.today()

    # create distribution plans
    for i in range(1, distribution_plans + 1):
        number = i
        DistributionPlan(
            version="%s.0" % number,
            valid_from=today
        ).save()
