import serial
import time
#self.port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

class comm:

	def __init__(self):
		self.holdon = 5

	def connect(self):
		try:
			self.port = serial.Serial("/dev/ttyGS0", baudrate=9600, timeout=self.holdon)
		except serial.serialutil.SerialException:
			self.port.close()
			self.port.open()
		return self.port

	def disconnect(self):
		self.port.close()
		return self.port

	def send_data(self, header, data, wait_for_confirmation = True, timeout = 30, validate_data = False):
		keeptrying = True
		payload = header + ":" + str(data) + "\n"
		while keeptrying:
			try:
				self.port.write(payload.encode())
			except:
				return False
			if not wait_for_confirmation:
				return True
			#time.sleep(self.holdon)
			timeout = timeout - self.holdon
			if validate_data:
				resp = wait_data(header + "_ok", 0)
				if resp == str(data):
					return True
			else:
				if self.wait_ok():
					return True
			#print("No right response: ", resp)
			keeptrying = wait_for_confirmation and (timeout>0)
		return False

	def wait_data(self, header, timeout=30):
		while timeout>=0:
			line = self.port.readline().decode("utf-8").replace("\n","")
			#print("Line read: ", line)
			indx = line.find(":")
			if indx >= 0 and line[0:indx]==header:
				return line[indx+1:]
			timeout = timeout - self.holdon
		return ""
	    
	def wait_ok(self, timeout=30):
		while timeout>=0:
			line = self.port.readline().decode("utf-8").replace("\n","")
			#print("Line read: ", line)
			if line == "ok":
				return True
			timeout = timeout - self.holdon
		return False    

	def send_xpub(self, xpub, wid, devid):
		if self.send_data("xpub", xpub):
			if self.send_data("wid", wid):
				if self.send_data("devid", devid):
					return True
		return False

	def get_unsigned(self):
		self.send_data("get", "unsigned", False)
		return wait_data("unsigned")

	def get_pin(self):
		self.send_data("get", "pin", False)
		return wait_data("pin")

	def send_signed(self, hexdata):
		if self.send_data("signed", hexdata):
			return True
		return False