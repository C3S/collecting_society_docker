# flake8: noqa: E501

allocations_collected = Allocation.search(['state', '=', 'collected'])

session_id, _, _ = Distribute.create()
_distribute = Distribute(session_id)
_distribute.start.allocations = allocations_collected
_distribute.start.entity_origin = 'manually'
_distribute.transition_distribute()

distribution = allocations_collected[0].distribution
