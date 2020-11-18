from .Contract import Contract
from .Enums import *


class ModicumV2Contract(Contract):

	def setup(self, from_account, getReceipt, _mediationCost, _allocationCost, _penaltyRate, _signTimeOut, _mediationTimeOut):
		return self.call_func(from_account, getReceipt, 0, "setup", 
			"uint", _mediationCost,
			"uint", _allocationCost,
			"uint", _penaltyRate,
			"uint", _signTimeOut,
			"uint", _mediationTimeOut
		)

	def test(self, from_account, getReceipt):
		return self.call_func(from_account, getReceipt, 0, "test"
			
		)

	def changeState(self, from_account, getReceipt, allocationID, newState):
		return self.call_func(from_account, getReceipt, 0, "changeState", 
			"uint", allocationID,
			"State", newState
		)

	def sendEther(self, from_account, getReceipt, target, value, reason):
		return self.call_func(from_account, getReceipt, 0, "sendEther", 
			"address", target,
			"uint", value,
			"EtherSendReason", reason
		)

	def sign(self, from_account, getReceipt, allocationID):
		return self.call_func(from_account, getReceipt, 0, "sign", 
			"uint", allocationID
		)

	def hash(self, from_account, getReceipt, object):
		return self.call_func(from_account, getReceipt, 0, "hash", 
			"bytes32", object
		)

	def createAllocation(self, from_account, getReceipt, value, customer, mediator, customerOfferHash, outputHashHash):
		return self.call_func(from_account, getReceipt, 0, "createAllocation", 
			"uint", value,
			"address", customer,
			"address", mediator,
			"bytes32", customerOfferHash,
			"bytes32", outputHashHash
		)

	def addSupplier(self, from_account, getReceipt, allocationID, supplier, offerHash, done):
		return self.call_func(from_account, getReceipt, 0, "addSupplier", 
			"uint", allocationID,
			"address", supplier,
			"bytes32", offerHash,
			"bool", done
		)

	def mediatorSign(self, from_account, getReceipt, allocationID):
		return self.call_func(from_account, getReceipt, 0, "mediatorSign", 
			"uint", allocationID
		)

	def supplierSign(self, from_account, getReceipt, price, allocationID, supplierID):
		return self.call_func(from_account, getReceipt, price, "supplierSign", 
			"uint", allocationID,
			"uint", supplierID
		)

	def customerSign(self, from_account, getReceipt, price, allocationID):
		return self.call_func(from_account, getReceipt, price, "customerSign", 
			"uint", allocationID
		)

	def postOutput(self, from_account, getReceipt, allocationID, supplierID, outputHash):
		return self.call_func(from_account, getReceipt, 0, "postOutput", 
			"uint", allocationID,
			"uint", supplierID,
			"bytes32", outputHash
		)

	def postMediation(self, from_account, getReceipt, allocationID, outputHashHash):
		return self.call_func(from_account, getReceipt, 0, "postMediation", 
			"uint", allocationID,
			"bytes32", outputHashHash
		)

	def clearMarket(self, from_account, getReceipt, allocationID):
		return self.call_func(from_account, getReceipt, 0, "clearMarket", 
			"uint", allocationID
		)

	def returnDeposits(self, from_account, getReceipt, allocationID):
		return self.call_func(from_account, getReceipt, 0, "returnDeposits", 
			"uint", allocationID
		)

	def __init__(self, client, address):
		super().__init__(client, address, {'AllocationCreated': [('value', 'uint'), ('allocator', 'address'), ('customer', 'address'), ('mediator', 'address'), ('customerOfferHash', 'bytes32'), ('outputHash', 'bytes32'), ('id', 'uint')], 'StateChanged': [('allocationID', 'uint'), ('newState', 'State')], 'MediationRequested': [('allocationID', 'uint')], 'MediationCompleted': [('allocationID', 'uint'), ('outputHashHash', 'bytes32')], 'VerifierAccepted': [('allocationID', 'uint')], 'ParametersSet': [('mediationCost', 'uint'), ('_erificationCost', 'uint'), ('allocationCost', 'uint'), ('penaltyRate', 'uint')], 'EtherSend': [('target', 'address'), ('value', 'uint'), ('reason', 'EtherSendReason')], 'Setup': [('mediationCost', 'uint'), ('allocationCost', 'uint'), ('penaltyRate', 'uint'), ('_signTimeOut', 'uint'), ('_mediationTimeOut', 'uint')], 'OutputPosted': [('allocationID', 'uint'), ('supplierID', 'uint'), ('outputHash', 'bytes32')], 'TestUint': [('x', 'uint')], 'TestEnum': [('state', 'State')], 'TestBool': [('x', 'bool')], 'SupplierAdded': [('allocationID', 'uint'), ('supplierID', 'uint'), ('supplier', 'address'), ('offerHash', 'bytes32')], 'Log': [('hash', 'bytes32')]})
