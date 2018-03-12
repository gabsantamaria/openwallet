import subprocess
import os.path
from collections import namedtuple
from pathlib import Path

Config = namedtuple('Config', 'binary_cmd, default_wdir, max_wid')
conf = Config("elefork", str(Path(os.getcwd()).parents[1]), 100)

def get_free_wid(wdir = ""):
	global conf
	for wid in range(1,conf.max_wid + 1):
		if not os.path.exists(get_full_wpath(wid, wdir)):
			return wid
	return 0

def run(args):
	return subprocess.run(args, stdout=subprocess.PIPE)

def get_full_wpath(wid, wdir):
	global conf
	if wdir == "":
		return conf.default_wdir + "/wallet" + str(wid)
	else:
		return wdir + "/wallet" + str(wid)

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
