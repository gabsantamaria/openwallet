import wallet_screens as sc
import wallet_subs as sub
import wrapper as core
from commusb import comm

com = comm()

def turn_on():
	sc.initialize()
	sc.initializing()
	sub.init_on_firsttime()
	while core.get_num_wids() == 0:
		#no wallets created
		sub.create_new_wallet()
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
	return 0

def exchange_data():
	return 0