#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Modify the products
"""

from proteus import Model

DEPENDS = [
    'product_template'
]


def generate(reclimit=0):

    # models
    Product = Model.get('product.product')

    # entries
    products = Product.find()

    # modify products
    for product in products:
        product.code = product.name[0]
        product.description = product.name
        product.active = True
        product.save()
