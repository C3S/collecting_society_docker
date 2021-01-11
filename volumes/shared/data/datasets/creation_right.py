#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the creation rights
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'creation',
    'collecting_society',
    'instrument',
]


def generate(reclimit=0):

    # constants
    max_composers_per_creation = reclimit or 3
    min_composers_per_creation = reclimit and 1 or 0
    # max_recorders_per_creation = reclimit or 3
    # min_recorders_per_creation = reclimit and 1 or 0
    max_interprets_per_creation = reclimit or 3
    min_interprets_per_creation = reclimit and 1 or 0
    max_instruments_per_interpret = reclimit or 3
    max_texters_per_creation = reclimit or 2
    min_texters_per_creation = reclimit and 1 or 0
    max_producers_per_creation = reclimit or 2
    min_producers_per_creation = reclimit and 1 or 0
    max_masters_per_creation = reclimit or 2
    min_masters_per_creation = reclimit and 1 or 0
    max_mixers_per_creation = reclimit or 2
    min_mixers_per_creation = reclimit and 1 or 0
    collecting_society_per_creationright = reclimit and 1 or 0.3
    successor_chance_per_right = reclimit and 1 or 0.1

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    CollectingSociety = Model.get('collecting_society')
    Instrument = Model.get('instrument')
    CreationRight = Model.get('creation.right')
    Country = Model.get('country.country')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    all_artists = Artist.find([])
    crss = CollectingSociety.find([(
        'represents_copyright', '=', True)])
    nrss = CollectingSociety.find([(
        'represents_ancillary_copyright', '=', True)])
    total_number_of_instruments = len(Instrument.find([]))
    germany, = Country.find([('code', '=', 'DE')])

    # content
    today = datetime.date.today()

    def make_successor(creation, pre):
        if random.random() > successor_chance_per_right:
            return
        suc = creation.rights.new()
        suc.rightsholder = random.choice(all_artists)
        suc.rightsobject = pre.rightsobject
        suc.contribution = pre.contribution
        suc.type_of_right = pre.type_of_right
        suc.valid_from = pre.valid_from
        suc.country = germany
        if random.random() < collecting_society_per_creationright:
            suc.collecting_society = crss[random.randint(0, len(crss)-1)]
        if pre.instruments:
            pre_inst_ids = [inst.id for inst in pre.instruments]
            pre_inst = Instrument.find([('id', 'in', pre_inst_ids)])
            suc.instruments.extend(pre_inst)
        suc.save()
        pre.successor = suc
        pre.valid_from = suc.valid_from - datetime.timedelta(
            days=random.randint(0, 36500))
        pre.valid_to = suc.valid_from

    # create creation rights
    for creation in creations:
        artist = creation.artist
        rightsholders = [artist]
        if artist.group:
            rightsholders = artist.solo_artists
        creation_date = today - datetime.timedelta(
            days=random.randint(0, 36500))

        # composer
        num_composers = random.randint(min_composers_per_creation, min(
            max_composers_per_creation, len(rightsholders)))
        for composer in random.sample(rightsholders, num_composers):
            cr = creation.rights.new()
            cr.rightsholder = composer
            cr.contribution = 'composition'
            cr.type_of_right = 'copyright'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = random.choice(crss)
            make_successor(creation, cr)

        # texters
        num_texters = random.randint(min_texters_per_creation, min(
            max_texters_per_creation, len(rightsholders)))
        for texter in random.sample(rightsholders, num_texters):
            cr = creation.rights.new()
            cr.rightsholder = texter
            cr.contribution = 'lyrics'
            cr.type_of_right = 'copyright'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(crss)-1)]
            make_successor(creation, cr)

        # interprets
        num_interprets = random.randint(min_interprets_per_creation, min(
            max_interprets_per_creation, len(rightsholders)))
        num_instruments = random.randint(1, min(
            max_instruments_per_interpret, total_number_of_instruments))
        for interpret in random.sample(rightsholders, num_interprets):
            cr = creation.rights.new()
            cr.rightsholder = interpret
            cr.contribution = 'instrument'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(nrss)-1)]
            instruments = Instrument.find([])
            cr.instruments.extend(random.sample(instruments, num_instruments))
            make_successor(creation, cr)

        # producer
        num_producers = random.randint(min_producers_per_creation, min(
            max_producers_per_creation, len(rightsholders)))
        for producer in random.sample(rightsholders, num_producers):
            cr = creation.rights.new()
            cr.rightsholder = producer
            cr.contribution = 'production'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(crss)-1)]
            make_successor(creation, cr)

        # master
        num_masters = random.randint(min_masters_per_creation, min(
            max_masters_per_creation, len(rightsholders)))
        for master in random.sample(rightsholders, num_masters):
            cr = creation.rights.new()
            cr.rightsholder = master
            cr.contribution = 'mastering'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(crss)-1)]
            make_successor(creation, cr)

        # mixer
        num_mixers = random.randint(min_mixers_per_creation, min(
            max_mixers_per_creation, len(rightsholders)))
        for mixer in random.sample(rightsholders, num_mixers):
            cr = creation.rights.new()
            cr.rightsholder = mixer
            cr.contribution = 'mixing'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(crss)-1)]
            make_successor(creation, cr)

        creation.save()

    # TODO: recorders?

    # TODO: foreign rightsholders
