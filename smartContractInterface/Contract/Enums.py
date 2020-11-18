from enum import Enum


class State(Enum):
	Allocated = 0
	Signing = 1
	Running = 2
	Close = 3


class EtherSendReason(Enum):
	Payroll = 0
	MediationCost = 1
	AllocationCost = 2
	Refund = 3
	JobCancelled = 4

