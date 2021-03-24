#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the products
"""

from proteus import Model

DEPENDS = [
    'product_template'
]


def generate(reclimit=0):

    # models
    ProductTemplate = Model.get('product.template')
    Product = Model.get('product.product')

    # entries
    templates = ProductTemplate.find()

    # create products
    for template in templates:
        product = Product()
        product.template = template
        product.code = template.name[0]
        product.description = template.name
        product.active = True
        product.save()
