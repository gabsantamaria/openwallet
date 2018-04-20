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
	#sc.write_text("             cool", 54)
	while core.get_num_wids() == 0:
		#no wallets created
		print("core.get_num_wids()", core.get_num_wids())
		no_wallet()
	wids = core.get_list_wid()
	me.loaded_wid = wids[0]
	#sc.write_text("loaded: " + str(me.loaded_wid), 35)
	me.loaded_xpub = core.get_mpk(me.loaded_wid)
	#sc.write_text("xpub: " + str(me.loaded_xpub), 45)
	wait_for_action()
	sub.shut_down()
	return 0

def no_wallet():
	sc.creating()
	new_seed = core.create_seed()
	if new_seed == "":
		return False
	else:
		if sc.show_seed(new_seed):
			pin = sc.chose_pin()
			if pin == False:
				return False
			free_wid = core.get_free_wid()
			sc.saving_wallet(free_wid)
			core.create_from_seed(new_seed, free_wid, pin)
			sc.saved_wallet(free_wid)
			return True
		else:
			return False


def wait_for_action():
	#TODO wait also for actions like creating or deleting wallets
	#sc.write_text("entered: ", 55)
	while True:
		if wait_for_connection():
			unsigned_txn = wait_for_transaction()
			if not unsigned_txn == None:
				verified = verify_transaction(unsigned_txn)
				if not verified == None:
					signed_txn = wait_for_signing(unsigned_txn)
					if not signed_txn == None:
						print("Successful operation")
					
	return 0

def wait_for_transaction():
	sc.waiting_transaction(me.loaded_wid)
	unsigned_txn = me.com.get_unsigned()
	while unsigned_txn == "":
		time.sleep(1)
		unsigned_txn = me.com.get_unsigned()
	return unsigned_txn

def verify_transaction(unsigned_txn):
	sc.verifying_transaction(me.loaded_wid)
	txn_info = core.verify_transaction(unsigned_txn, me.loaded_wid)
	print(txn_info)
	if txn_info == None:
		sc.invalid_transaction(me.loaded_wid)
		return None
	payees = txn_info['payees']
	amount = txn_info['amount_no_fee']
	foreign_inputs = txn_info['foreign_inputs']
	total_out = txn_info['total_out']
	payers = txn_info['payers']
	if foreign_inputs>0 or len(payees)>1:
		print("Invalid txn. Recall foreign inputs and multiple payees are not allowed")
		sc.invalid_transaction(me.loaded_wid)
		return None
	else:
		if sc.transaction_info(payees[0], amount, me.loaded_wid): #accepted
			return {"payee":payees[0], "amount": amount, "txn_info": txn_info}
		else:
			return None

def wait_for_signing(unsigned_txn):
	signed_txn = -1
	trials_left = 3
	scrambled = [0,1,2,3,4,5,6,7,8,9]
	#print("original scrambled: ", scrambled)
	while signed_txn == -1 and trials_left > 0:
		random.shuffle(scrambled)
		print("now scrambled: ", scrambled)
		sc.scrambled_numpad(scrambled)
		retrieved_pin = me.com.get_pin()
		while retrieved_pin == "":
			retrieved_pin = me.com.get_pin()
			time.sleep(1)
		if retrieved_pin == "cancel":
			return None
		sc.signing(me.loaded_wid)
		pwd = ""
		for digit in retrieved_pin:
			pwd = pwd + str(scrambled[int(digit)])
		signed_txn = core.sign_transaction(unsigned_txn, me.loaded_wid, pwd)
		trials_left -= 1
	if signed_txn == -1:
		return None
	if me.com.send_signed(signed_txn) == False:
		print("Signed successfully, but no response from USB after sending")
		return None
	return signed_txn

def wait_for_connection():
	sc.waiting_connection(me.loaded_wid)
	me.com.connect()
	#sc.connecting(me.loaded_wid)
	if not me.com.send_xpub(me.loaded_xpub, me.loaded_wid, me.devid):
		me.com.disconnect()
		print("Could not connect and get response, trying again")
		return False
	return True




