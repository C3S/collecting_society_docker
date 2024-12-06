# flake8: noqa: E501

utilsations_finalized = Utilisation.search(['state', '=', 'finalized'])

session_id, _, _ = Collect.create()
_collect = Collect(session_id)
_collect.start.utilisations = utilsations_finalized[:4]
_collect.start.entity_origin = 'manually'
_collect.transition_collect()

collection = utilsations_finalized[0].collection
pprint(f"collection utilisations: {collection.utilisations}")

for allocation in collection.allocations:
    pprint({
        'allocation': allocation,
        'state': allocation.state,
        'invoice_amount': allocation.invoice_amount,
        'administration_fee': allocation.administration_fee,
        'distribution_amount': allocation.distribution_amount,
        'utilisations': [{
            'invoice_amount': utilisation.confirmed_invoice_amount,
            'administration_fee': utilisation.confirmed_administration_fee,
            'distribution_amount': utilisation.confirmed_distribution_amount,
        } for utilisation in allocation.utilisations]
    })

allocation = collection.allocations[0]
licensee = allocation.licensee
invoice = allocation.invoice
