import wallet_screens as sc
import wallet_subs as sub
import wrapper as core
from commusb import comm
import time
import random

class Me:
	pass
me = Me()

me.loaded_wid = None
me.devid = "naf7asfd4f9dg"
me.loaded_xpub = None

def turn_on():
	me.com = comm()
	sc.initialize()
	sc.initializing()
	sub.init_on_firsttime()
	while core.get_num_wids() == 0:
		#no wallets created
		sub.create_new_wallet()
	wids = core.get_list_wid()
	me.loaded_wid = wids[0]
	me.loaded_xpub = core.get_mpk(me.loaded_wid)
	wait_for_action()
	sub.shut_down()
	return 0

def wait_for_action():
	#TODO wait also for actions like creating or deleting wallets
	while True:
		wait_for_connection()
	return 0

def wait_for_connection():
	sc.waiting_connection(me.loaded_wid)
	me.com.connect()
	#sc.connecting(me.loaded_wid)
	while not me.com.send_xpub(me.loaded_xpub, me.loaded_wid, me.devid):
		time.sleep(1)
	sc.waiting_transaction(me.loaded_wid)

	unsigned_txn = me.com.get_unsigned()
	while unsigned_txn == "":
		time.sleep(1)
		unsigned_txn = me.com.get_unsigned()
	sc.verifying_transaction(me.loaded_wid)
	txn_info = core.verify_transaction(unsigned_txn, me.loaded_wid)
	print(txn_info)
	payees = txn_info['payees']
	amount = txn_info['amount_no_fee']
	foreign_inputs = txn_info['foreign_inputs']
	total_out = txn_info['total_out']
	payers = txn_info['payers']
	if foreign_inputs>0 or len(payees)>1:
		print("Invalid txn. Recall foreign inputs and multiple payees are not allowed")
		sc.invalid_transaction(me.loaded_wid)
		return False
	if not sc.transaction_info(payees[0], amount, me.loaded_wid): #rejected
		return False
	signed_txn = -1
	trials_left = 3
	while signed_txn == -1 and trials_left > 0:
		scrambled = random.shuffle([0,1,2,3,4,5,6,7,8,9])
		sc.scrambled_numpad(scrambled)
		retrieved_pin = me.com.get_pin()
		while retrieved_pin == "":
			retrieved_pin = me.com.get_pin()
			time.sleep(1)
		if retrieved_pin == "cancel":
			return False
		pwd = ""
		for digit in retrieved_pin:
			pwd = pwd + scrambled[digit]
		signed_txn = core.sign_transaction(unsigned_txn, me.loaded_wid, pwd)
		trials_left -= 1
	if signed_txn == -1:
		return False
	if send_signed(signed_txn) == False:
		return False
	return True
