import wallet_screens as sc
import wallet_subs as sub
import wrapper as core
from commusb import comm
import time

com = comm()
loaded_wid = None
devid = "naf7asfd4f9dg"

def turn_on():
	sc.initialize()
	sc.initializing()
	sub.init_on_firsttime()
	while core.get_num_wids() == 0:
		#no wallets created
		sub.create_new_wallet()
	wids = get_list_wid()
	loaded_wid = wids[0]
	wait_for_action()
	sub.shut_down()
	return 0

def wait_for_action():
	#TODO wait also for actions like creating or deleting wallets
	wait_for_connection()
	return 0

def wait_for_connection():
	sc.waiting_connection()
	com.connect()
	
	while not con.send_xpub(core.get_mpk(loaded_wid), loaded_wid, devid):
		time.sleep(1)
	sc.waiting_transaction()
	return 0

def exchange_data():
	return 0