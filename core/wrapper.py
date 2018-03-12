

import sys
import subprocess
import os.path
from collections import namedtuple
from pathlib import Path
import time

sys.path.append("/usr/local/lib/python3.6/dist-packages/electrum")

from electrum.wallet import Wallet, Imported_Wallet
from electrum.commands import get_parser, known_commands, Commands, config_variables
from electrum.storage import WalletStorage, get_derivation_used_for_hw_device_encryption
from electrum import SimpleConfig, Network
#from .transaction import Transaction, multisig_script




Config = namedtuple('Config', 'binary_cmd, default_wdir, max_wid')
conf = Config("elefork", str(Path(os.getcwd()).parents[1]), 100)

def sign(wid, wdir = ""):
	tx = """{
    "final": true,
    "hex": "010000000110c5d3408e11dc7d1327f3f2e0e789cce8c578209ed053ddf0a7285a48464811010000005701ff4c53ff0488b21e00000000000000000072206531a8760a41dca79069867623438f731ca96c7638e74ddfb5f6e1e64840027d186e91738ad1d8e4bec6ecf35095022b5d8cc131cb5d0b3794680b84f8dcc700000000feffffff0250c30000000000001976a914169bef354fd03ed4ae370a733389d58bd6a9dbf988ac54e60100000000001976a914d97c68e0a9619e7d53d6f8bb0bd7f7d34ffbe33b88ac92d40700",
    "complete": false
	}"""
	#tx = Transaction(tx)
	wpath = get_full_wpath(wid, wdir)
	ws = WalletStorage(wpath)
	wallet = Imported_Wallet(ws)
	cmd = Commands(SimpleConfig(), wallet, None)
	sgnd = cmd.signtransaction(tx, None, "1520")
	#wallet.sign_transaction(tx, password)
	print(sgnd)
	#return sgnd

def run(args):
	return subprocess.run(args, stdout=subprocess.PIPE)

def get_full_wpath(wid, wdir, onlyparent=False):
	global conf
	if wdir == "":
		if not onlyparent:
			return conf.default_wdir + "/wallet" + str(wid)
		else:
			return conf.default_wdir
	else:
		if not onlyparent:
			return wdir + "/wallet" + str(wid)
		else:
			return wdir

def get_free_wid(wdir = ""):
	global conf
	for wid in range(1,conf.max_wid + 1):
		if not os.path.exists(get_full_wpath(wid, wdir)):
			return wid
	return 0

def create_seed():
	global conf
	res = run([conf.binary_cmd, "make_seed"])
	if (res.returncode == 0):
		seed = str(res.stdout[0:-1])
		seed = seed[2:-1]
		return seed
	else:
		return ""

def create_from_seed(seed, wid, pwd = None, wdir = ""):
	global conf
	if wid == 0:
		return 1
	comm = [conf.binary_cmd, "restore", "-o", "-w", get_full_wpath(wid, wdir), seed]
	if pwd != None:
		comm.append("-encpwd")
		comm.append(str(pwd))
	res = run(comm)
	print (res)
	print ("Save the following seed!: " + seed)
	return 0

def get_mpk(wid, wdir = ""):
	global conf
	res = run([conf.binary_cmd, "getmpk", "-w", get_full_wpath(wid, wdir)])
	if (res.returncode == 0):
		mpk = str(res.stdout)
		return mpk[2:-3]
	else:
		return ""

def sign_transaction(unsigned_txn, wid, pwd = None, wdir = ""):
	global conf
	if os.path.isfile(unsigned_txn):
		usg_path = unsigned_txn
	else:
		usg_path = get_full_wpath(wid, wdir, True) + "/temp_unsigned.txn"
		temp_usg = open(usg_path, "w")
		temp_usg.write(unsigned_txn)
		temp_usg.close()	

	sgn_path = get_full_wpath(wid, wdir, True) + "/temp_signed.txn"
	comm = ['cat', usg_path, '|', 'elefork','signtransaction', '-w', get_full_wpath(wid, wdir)]
	#comm = [unsigned_txn, 'elefork','signtransaction', '-w', get_full_wpath(wid, wdir)]
	if pwd != None:
		comm.append("-encpwd")
		comm.append(str(pwd))
	comm.append('->')
	comm.append(sgn_path)
	#cat = subprocess.Popen(('cat', 'unsigned.txn'), stdout=subprocess.PIPE)
	#output = subprocess.check_output(comm, stdin=cat.stdout)
	#cat.wait()
	#comm = "cat /home/gsant/Dropbox/JAG_LY/walletside/openwallet/core/unsigned.txn | elefork signtransaction -w " + get_full_wpath(wid, wdir) + " -encpwd 1520 -> /home/gsant/Dropbox/JAG_LY/walletside/openwallet/core/signed.txn"
	comm = " ".join(comm)
	cat = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()

	timeout = 10
	while (not os.path.isfile(sgn_path)) and (timeout>0):
		time.sleep(0.1)
		timeout = timeout - 0.1

	if timeout > 0:
		with open(sgn_path, 'r') as content_sgn:
			temp_sgn = content_sgn.read()
		return temp_sgn
	else:
		return -1