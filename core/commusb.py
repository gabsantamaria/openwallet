import serial
import time
#port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
holdon = 5

port = None

def initialize():
	port = serial.Serial("/dev/ttyGS0", baudrate=9600, timeout=holdon)
	return port

def send_data(header, data, wait_for_confirmation = True, timeout = 30, validate_data = False):
	keeptrying = True
	payload = header + ":" + data + "\n"
	while keeptrying:
		port.write(payload.encode())
		if not wait_for_confirmation:
			return True
		#time.sleep(holdon)
		timeout = timeout - holdon
		if validate_data:
			resp = wait_data(header + "_ok", 0)
			if resp == data:
				return True
		else:
			if wait_ok():
				return True
		#print("No right response: ", resp)
		keeptrying = wait_for_confirmation and (timeout>0)
	return False

def wait_data(header, timeout=30):
	while timeout>=0:
		line = port.readline().decode("utf-8").replace("\n","")
		#print("Line read: ", line)
		indx = line.find(":")
		if indx >= 0 and line[0:indx]==header:
			return line[indx+1:]
		timeout = timeout - holdon
	return ""
    
def wait_ok(timeout=30):
	while timeout>=0:
		line = port.readline().decode("utf-8").replace("\n","")
		#print("Line read: ", line)
		if line == "ok":
			return True
		timeout = timeout - holdon
	return False    

def send_xpub(xpub, wid, devid):
	if send_data("xpub", xpub):
		if send_data("wid", wid):
			if send_data("devid", devid):
				return True
	return False

def get_unsigned():
	send_data("get", "unsigned", False)
	return wait_data("unsigned")

def get_pin():
	send_data("get", "pin", False)
	return wait_data("pin")

def send_signed(hexdata):
	if send_data("signed", hexdata):
		return True

	return False