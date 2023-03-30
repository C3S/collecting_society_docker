#!/usr/bin/env python
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Prints infos on the models of the collecting_society module.

Usage:

    ./modelinfo.py
"""

import os
import csv
from inspect import getmembers, isclass, getmro
import trytond.modules.collecting_society as cs

BASE_CLASSES = [
    'ModelSQL',
    'ModelView',
    'Wizard',
]


# get model info
model_info = []
for name, cls in getmembers(cs, isclass):
    tryton_id = getattr(cls, '__name__', False)
    if not tryton_id or name == tryton_id:
        continue
    tryton_base_classes = [
        basecls.__name__
        for basecls in getmro(cls)
        if basecls.__name__ in BASE_CLASSES
    ]
    if not tryton_base_classes:
        continue
    model_info.append({
        "Type": ", ".join(tryton_base_classes),
        "Class": name,
        "Id": tryton_id
    })


# print model info
def size(key):
    return len(max([row[key] for row in model_info], key=len)) + 3


columns = ['Type', 'Class', 'Id']
sizes = []
for column in columns:
    sizes.append(size(column))
row = "{:%s}{:%s}{:%s}" % tuple(sizes)
print()
print(row.format(*columns))
print(row.format("-" * (sizes[0] - 2),
                 "-" * (sizes[1] - 2),
                 "-" * (sizes[2] - 2)))
for data in model_info:
    print(row.format(*data.values()))
print()

# write model info csv
path = os.path.dirname(os.path.abspath(__file__))
with open(f'{path}/modelinfo.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(model_info)
