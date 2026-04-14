#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the distribution plans
"""

import datetime
from dateutil.relativedelta import relativedelta

from proteus import Model

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    distribution_plans = min(reclimit or 3, 3)  # increase on new distr. plans

    # models
    DistributionPlan = Model.get('distribution.plan')

    # create distribution plans
    for i in range(1, distribution_plans + 1):
        number = i
        from_date = datetime.date.today() - relativedelta(
            years=distribution_plans-i
        )
        to_date = from_date + relativedelta(years=1) - relativedelta(days=1)
        if i == 1:
            from_date = None
        if i == distribution_plans:
            to_date = None
        DistributionPlan(
            version="0.%s" % number,
            valid_from=from_date,
            valid_through=to_date
        ).save()
