import serial

#port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
holdon = 5
port = serial.Serial("/dev/ttyGS0", baudrate=9600, timeout=holdon)


def send_data(header, data, wait_for_confirmation = True, timeout = 30):
	keeptrying = True
	payload = header + ":" + data + "\n"
	while keeptrying:
		port.write(payload.encode())
		if !wait_for_confirmation:
			return True
		#sleep(holdon)
		timeout = timeout - holdon
		resp = wait_data(header + "_ok", 0)
		if resp == data
			return True
		keeptrying = wait_for_confirmation and (timeout>0)
	return False

def wait_data(header, timeout=30):
	while timeout>0:
		line = repr(port.readline()).replace("\n","")
		indx = line.find(":")
		if indx >= 0 and line[0:indx]==header:
			return line[indx+1:]
		timeout = timeout - holdon
	return ""

def send_xpub(xpub, wid, devid):
	if send_data("Hello", "Hello"):
		if send_data("xpub", xpub):
			if send_data("wid", wid):
				if send_data("devid", devid):
					return True
	return False

def get_unsigned():
	return wait_data("unsigned")

def get_pin()
	return wait_data("pin")

def send_signed(hexdata):
	if send_data("signed", hexdata):
		return True

	return False