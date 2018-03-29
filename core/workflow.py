import wallet_screens as sc
import wallet_subs as sub
import wrapper as core
from commusb import comm
import time

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
	wait_for_connection()
	return 0

def wait_for_connection():
	sc.waiting_connection(me.loaded_wid)
	me.com.connect()
	#sc.connecting(me.loaded_wid)
	while not me.com.send_xpub(me.loaded_xpub, me.loaded_wid, me.devid):
		time.sleep(1)
	sc.waiting_transaction(me.loaded_wid)
	return 0

def exchange_data():
	return 0