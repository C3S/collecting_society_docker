# flake8: noqa: E501

web_user = WebUser(1)
tariff = Tariff(1)
period = 'onetime'
distribution_plan, = DistributionPlan.search([], 0, 1, [('id', 'DESC')])
location_category = LocationCategory(1)
country, = Country.search(['code', '=', 'DE'])
tariff_relevance_category = TariffRelevanceCategory(1)
tariff_adjustment_category, = TariffAdjustmentCategory.search(['code', '=', 'small'])

# location
_location = {
    'name': 'Location Name',
    'category': location_category,
    'public': False,
    'street': 'Location Street',
    'postal_code': '12345',
    'city': 'Location City',
    'country': country,
    'entity_origin': 'indirect',
    'entity_creator': web_user.party,
}
location, = Location.create([_location])

# event
_event = {
    'name': 'Event Name',
    'description': 'Event Description',
    'location': location,
    'performances': [],
    'estimated_start': datetime.now(),
    'estimated_end': datetime.now(),
    'estimated_attendants': 100,
    'estimated_max_attendants': 1000,
    'estimated_max_admission': D(10),
    'estimated_turnover_tickets': D(1000),
    'estimated_turnover_benefit': D(2000),
    'estimated_expenses_musicians': D(3000),
    'estimated_expenses_production': D(4000),
}
event, = Event.create([_event])

# tariff relevance
_tariff_relevance = {
    'category': tariff_relevance_category,
    'value': tariff_relevance_category.value_default,
}
taritt_relevance, = TariffRelevance.create([_tariff_relevance])

# declaration
_declaration = {
    'licensee': web_user.party,
    'state': 'submitted',
    'tariff': tariff,
    'period': period,
    'context': event,
    'utilisations': [('create', [{
        'licensee': web_user.party,
        'state': 'estimated',
        'tariff': tariff,
        'distribution_plan': distribution_plan,
        'context': event,
        'estimated_relevance': taritt_relevance,
        'estimated_adjustments': [('create', [{
            'category': tariff_adjustment_category,
            'value': tariff_adjustment_category.value_default,
        }])]
    }])]
}
declaration, = Declaration.create([_declaration])
print(declaration)
