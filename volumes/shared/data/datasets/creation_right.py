#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create creation right
"""

from proteus import  Model

import datetime
import random

DEPENDS = [
    'artist',
    'creation',
    'collecting_societies',
    'creation_roles_and_instruments'
]


def generate(reclimit):

    # constants
    max_composers_per_creation = reclimit or 3
    max_recorders_per_creation = reclimit or 3
    max_interprets_per_creation = reclimit or 3
    max_instruments_per_interpret = reclimit or 3
    max_texters_per_creation = reclimit or 2
    max_producers_per_creation = reclimit or 2
    max_masters_per_creation = reclimit or 2
    max_mixers_per_creation = reclimit or 2
    collecting_society_per_creationright = reclimit and 1 or 0.3
    successor_chance_per_right = reclimit and 1 or 0.1

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    CollectingSociety = Model.get('collecting_society')
    Instrument = Model.get('instrument')
    CreationRight = Model.get('creation.right')
    CreationRole = Model.get('creation.role')
    Country = Model.get('country.country')

    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    all_artists = Artist.find([])
    all_artists_number = len(all_artists)
    crss = CollectingSociety.find([(
        'represents_copyright', '=', True)])
    nrss = CollectingSociety.find([(
        'represents_ancillary_copyright', '=', True)])
    total_number_of_instruments = len(Instrument.find([]))
    germany, = Country.find([('code', '=', 'DE')])
    today = datetime.date.today()

    def make_successor(pre):
        if random.random() < successor_chance_per_right:
            suc = CreationRight()
            suc.rightsholder = random.choice(all_artists)
            suc.rightsobject = pre.rightsobject
            suc.contribution = pre.contribution
            suc.type_of_right = pre.type_of_right
            suc.valid_from = pre.valid_from
            suc.country = germany
            suc.predecessor = pre
            if random.random() < collecting_society_per_creationright:
                suc.collecting_society = crss[random.randint(0, len(crss)-1)]
            if pre.instruments:
                pre_inst_ids = [ inst.id for inst in pre.instruments ]
                pre_inst = Instrument.find([('id', 'in', pre_inst_ids)])
                suc.instruments.extend(pre_inst)
            suc.save()
            pre.successor = suc
            pre.valid_from = suc.valid_from - datetime.timedelta(days=
                        random.randint(0, 36500))
            pre.valid_to = suc.valid_from
            pre.save()
    # Existing solo or member artists::
    for i in range(0, len(creations)):
        creation = creations[i]
        artist = creation.artist
        rightsholders = [artist]
        if artist.group:
            rightsholders = artist.solo_artists
        roles = CreationRole.find([])
        creation_date = today - datetime.timedelta(days=
                        random.randint(0, 36500))

        # composer
        num_composers = random.randint(0, min(
            max_composers_per_creation, len(rightsholders)))
        for composer in random.sample(rightsholders, num_composers):
            # composition
            cr = CreationRight()
            cr.rightsholder = composer
            cr.rightsobject = creation
            cr.contribution = 'composition'
            cr.type_of_right = 'copyright'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0, len(crss)-1)]
            cr.save()
            make_successor(cr)

        # texters
        num_texters = random.randint(0, min(
            max_texters_per_creation, len(rightsholders)))
        for texter in random.sample(rightsholders, num_texters):
            cr = CreationRight()
            cr.rightsholder = texter
            cr.rightsobject = creation
            cr.contribution = 'lyrics'
            cr.type_of_right = 'copyright'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0,
                    len(crss)-1)]
            cr.save()
            make_successor(cr)

        # interprets
        num_interprets = random.randint(0, min(
            max_interprets_per_creation, len(rightsholders)))
        num_instruments = random.randint(1, min(
            max_instruments_per_interpret, total_number_of_instruments))
        for interpret in random.sample(rightsholders, num_interprets):
            cr = CreationRight()
            cr.rightsholder = interpret
            cr.rightsobject = creation
            cr.contribution = 'instrument'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0,
                    len(nrss)-1)]
            instruments = Instrument.find([])
            cr.instruments.extend(random.sample(instruments, num_instruments))
            cr.save()
            make_successor(cr)

        # producer
        num_producers = random.randint(0, min(
            max_producers_per_creation, len(rightsholders)))
        for producer in random.sample(rightsholders, num_producers):
            cr = CreationRight()
            cr.rightsholder = producer
            cr.rightsobject = creation
            cr.contribution = 'production'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0,
                    len(crss)-1)]
            cr.save()
            make_successor(cr)

        # master
        num_masters = random.randint(0, min(
            max_masters_per_creation, len(rightsholders)))
        for master in random.sample(rightsholders, num_masters):
            cr = CreationRight()
            cr.rightsholder = master
            cr.rightsobject = creation
            cr.contribution = 'mastering'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0,
                    len(crss)-1)]
            cr.save()
            make_successor(cr)

        # mixer
        num_mixers = random.randint(0, min(
            max_mixers_per_creation, len(rightsholders)))
        for mixer in random.sample(rightsholders, num_mixers):
            cr = CreationRight()
            cr.rightsholder = mixer
            cr.rightsobject = creation
            cr.contribution = 'mixing'
            cr.type_of_right = 'ancillary'
            cr.valid_from = creation_date
            cr.country = germany
            if random.random() < collecting_society_per_creationright:
                cr.collecting_society = crss[random.randint(0,
                    len(crss)-1)]
            cr.save()
            make_successor(cr)

    # TODO: recorders?

    # TODO: foreign rightsholders
