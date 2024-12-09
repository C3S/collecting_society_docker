# flake8: noqa: E501

allocations_collected = Allocation.search(['state', '=', 'collected'])

transaction._locked_tables.add(JournalPeriod._table)
session_id, start_state, end_state = Distribute.create()
Distribute.execute(session_id, {}, start_state)
Distribute.execute(session_id, {
    'start': {
        'allocations': allocations_collected,
        'entity_origin': 'manually',
    },
}, 'distribute')

distribution = allocations_collected[0].distribution
