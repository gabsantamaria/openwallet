try:
	import RPi.GPIO as GPIO

	import time

	import Adafruit_GPIO.SPI as SPI
	import Adafruit_SSD1306

	from PIL import Image
	from PIL import ImageDraw
	from PIL import ImageFont

	# Input pins:
	L_pin = 27 
	R_pin = 23 
	C_pin = 4 
	U_pin = 17 
	D_pin = 22 

	A_pin = 5 
	B_pin = 6 

	RST = 24
	DC = 23
	SPI_PORT = 0
	SPI_DEVICE = 0
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	width = disp.width
	height = disp.height

	# Get drawing object to draw on image.
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)

	# Load default font.
	font = ImageFont.load_default()
	fontnumpad = ImageFont.truetype('m04.ttf',8)
	# Draw some shapes.
	# First define some constants to allow easy resizing of shapes.
	padding = -2
	top = padding
	bottom = height-padding
	# Move left to right keeping track of the current x position for drawing shapes.
	x = 0
except Exception:
	print ("There was an error in screens module")

def clear_disp():
	try:
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		disp.image(image)
		disp.display()
	except Exception:
		print ("There was an error in screens module")
	return 0

def initialize():
	try:
		GPIO.setmode(GPIO.BCM) 
		GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
		# Initialize library.
		disp.begin()

		# Clear display.
		disp.clear()
		disp.display()

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

		# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
		# Some other nice fonts to try: http://www.dafont.com/bitmap.php
		# font = ImageFont.truetype('Minecraftia.ttf', 8)
	except Exception:
		print ("There was an error in screens module")
	return 0

def write_text(text, yval=top, npad = False, xval=x):
	try:
		if npad:
			thefont = fontnumpad
		else:
			thefont = font
		draw.text((xval, yval), str(text), font=thefont, fill=255)
		disp.image(image)
		disp.display()
	except Exception:
		print ("There was an error in screens module")

def initializing():
	clear_disp()
	write_text("Initializing wallet...", top + 16)
	write_text("Please wait", top + 25)
	return 0

def new_wallet(seed):
	return 0

def indicate_wloaded(loaded_wid = ""):
	try:
		if loaded_wid == "":
			return 0
		draw.line([0, 64-9-2, 16, 64-9-2], fill=1)
		disp.image(image)
		disp.display()
		write_text("W" + str(loaded_wid), 64-8-1)
	except Exception:
		print ("There was an error in screens module")
	return 0

def waiting_connection(loaded_wid = ""):
	clear_disp()
	write_text("Waiting for USB", top + 16)
	write_text("connection...", top + 25)
	write_text("               " + "cancel", top + 54)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	return 0

def connecting(loaded_wid = ""):
	clear_disp()
	write_text("connecting...", top + 16)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	return 0

def waiting_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Connected", top)
	write_text("Waiting for", top + 16)
	write_text("transaction...", top + 25)
	write_text("               " + "cancel", top + 54)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	return 0

def input_pin():
	return 0

def verifying_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Transaction received", top)
	write_text("Verifying...", top + 16)
	write_text("Please wait...", top + 25)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	return 0

def invalid_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Invalid transaction", top + 16)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	write_text("                 exit", top + 16 + 8)
	action = listenAB()
	while not listenAB() == "B":
		pass
	return True

def listenAB():
	try:
		try:
			while 1:
				if not GPIO.input(A_pin): # button [no] is pressed:
					while not GPIO.input(A_pin):
						pass
					return "A"
				if not GPIO.input(B_pin): # button [yes] is pressed:
					while not GPIO.input(B_pin):
						pass
					return "B"
		except KeyboardInterrupt: 
			GPIO.cleanup()
			return "err"
	except Exception:
		print ("There was an error in screens module")

def button_status():
	stat = ""
	if not GPIO.input(A_pin): # button [no] is pressed:
		stat = stat + "A"
	if not GPIO.input(B_pin): # button [yes] is pressed:
		stat = stat + "B"
	return stat

def transaction_info(payee_addr, amount, loaded_wid = ""):
	clear_disp()
	write_text("Pay to:", top)
	addr = str(payee_addr)
	cut1 = len(addr)//2
	write_text(addr[0:cut1], top + 8)
	write_text(addr[cut1:], top + 16)
	write_text("                  yes", top + 16 + 8)
	write_text(str(int(str(amount))/100000) + " mBTC", top + 34)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)
	write_text("                   no", top + 54)
	action = listenAB()
	if action == "B":
		return True
	else:
		return False

def scrambled_numpad(numbers):
	clear_disp()
	#print("numbers: ", numbers)
	sep = "  "
	line1 = str(numbers[1]) + sep + str(numbers[2]) + sep + str(numbers[3]) + sep + "Introd."
	line2 = str(numbers[4]) + sep + str(numbers[5]) + sep + str(numbers[6]) + sep + "  PIN"
	line3 = str(numbers[7]) + sep + str(numbers[8]) + sep + str(numbers[9])
	line4 = " " + sep + str(numbers[0])
	write_text(line1, 4 + top, True)
	write_text(line2, 4 + top + 16, True)
	write_text(line3, 4 + top + 32, True)
	write_text(line4, 4 + top + 48, True)
	write_text("               " + "cancel", top + 54)

def signing(loaded_wid):
	clear_disp()
	write_text("Signing transaction", top)
	write_text("Please wait...", top + 25)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	indicate_wloaded(loaded_wid)


def creating():
	clear_disp()
	write_text("Creating new wallet", top)
	write_text("Generating seed...", top + 25)
	write_text("Please wait...", top + 35)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)

def saving_wallet(wid):
	clear_disp()
	write_text("Saving new wallet", top)
	write_text("as W" + str(wid), top+10)
	write_text("Please wait...", top + 45)
	#write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)

def saved_wallet(wid):
	clear_disp()
	write_text("Wallet successfully", top)
	write_text("Created", top+10)
	write_text("             continue", top + 54)
	act = listenAB()
	return True

def loading_wallet():
	clear_disp()
	write_text("Loading wallet", top)
	write_text("Please wait...", top+10)
	return True

def show_seed(seed):
	words = seed.split()
	it = 0
	while (True):
		word = words[it]
		clear_disp()
		write_text("STORE THESE", top)
		write_text("WORDS SECURELY", top + 10)
		write_text(" -> " + str(word) + " <-", top + 35)
		write_text("      " + str(it+1) + "/12", top + 54)
		if it >= len(words) - 1:
			wnext = " end"
		else:
			wnext = "next"
		if it <= 0:
			wprev = "abort"
		else:
			wprev = " prev"
		write_text("                 " + wnext, top + 16 + 8)
		write_text("                " + wprev, top + 54)
		print("waiting for action...")
		act = listenAB()
		print("it = ", it)
		print("len(words) = ", len(words))
		if act == "B": #next
			if it >= len(words) - 1:
				return True
			it = it + 1
		else: #prev
			if it <= 0:
				return False
			else:
				it = it - 1

def chose_pin():
	current = ""
	it = 0
	options = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "reset", "cancel", "accept"]
	while (True):
		clear_disp()
		write_text("Choose pin", top)
		write_text("-> " + current + " <-", top + 10)
		write_text("                 " + "next", top + 16 + 8)
		write_text("                  " + "sel", top + 54)
		write_text("Choose: " + options[it], top + 35)
		act = listenAB()
		if act == "B": #next
			if it >= len(options) - 1:
				it = 0
			else:
				it = it + 1
		else: #select
			if it == 10:
				current = ""
			elif it == 11:
				return False
			elif it == 12:
				return current
			else:
				current = current + options[it]

def print_at(button, text):
	toprint = " "*(21-len(text)) + text
	if button == "B":
		write_text(toprint, top + 16 + 8)
	else:
		write_text(toprint, top + 54)

def main_screen(addr_info, loaded_wid):
	clear_disp()
	write_text("Receive at:", top)
	addr = str(addr_info)
	cut1 = len(addr)//2
	write_text(addr[0:cut1], top + 8)
	write_text(addr[cut1:], top + 16)
	print_at("B", "Connect")
	print_at("A", "Delete wallet")
	indicate_wloaded(loaded_wid)
	if listenAB() == "A":
		return "delete"
	else:
		return "connect"