# flake8: noqa: E501

live1 = Utilisation(5)
live2 = Utilisation(6)
live3 = Utilisation(7)

# calculations

def print_indicators(utilisation, sample='estimated'):
    samples = sample and [sample] or ['estimated', 'confirmed']
    fields = ['base', 'invoice_amount', 'administration_fee', 'distribution_amount']
    indicators = {}
    for sample in samples:
        if sample not in indicators:
            indicators[sample] = {}
        for field in fields:
            indicators[sample][field] = getattr(utilisation, f"{sample}_{field}")
    pprint(indicators)

print_indicators(live1, 'estimated')
live1.state = 'estimated'
live1.context.estimated_indicators.turnover_tickets += D(1000)
live1.calculate_base('estimated', save=True)
live1.calculate_invoice_amount('estimated', save=True)
live1.calculate_administration_fee('estimated', save=True)
print_indicators(live1, 'estimated')
