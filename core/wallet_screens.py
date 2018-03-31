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

def clear_disp():
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	disp.image(image)
	disp.display()
	return 0

def initialize():
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
	return 0

def write_text(text, yval=top, npad = False, xval=x):
	if npad:
		thefont = fontnumpad
	else:
		thefont = font
	draw.text((xval, yval), str(text), font=thefont, fill=255)
	disp.image(image)
	disp.display()

def initializing():
	clear_disp()
	write_text("Initializing wallet...", top + 16)
	write_text("Please wait", top + 25)
	return 0

def new_wallet(seed):
	return 0

def waiting_connection(loaded_wid = ""):
	clear_disp()
	write_text("Waiting for USB", top + 16)
	write_text("connection...", top + 25)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def connecting(loaded_wid = ""):
	clear_disp()
	write_text("connecting...", top + 16)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def waiting_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Connected", top)
	write_text("Waiting for", top + 16)
	write_text("transaction...", top + 25)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def input_pin():
	return 0

def verifying_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Transaction received", top)
	write_text("Verifying...", top + 16)
	write_text("Please wait...", top + 25)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def invalid_transaction(loaded_wid = ""):
	clear_disp()
	write_text("Invalid transaction", top + 16)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def transaction_info(payee_addr, amount, loaded_wid = ""):
	clear_disp()
	write_text("Pay to:", top)
	addr = str(payee_addr)
	cut1 = len(addr)//2
	write_text(addr[0:cut1], top + 8)
	write_text(addr[cut1:], top + 16)
	write_text(str(int(str(amount))/100000) + " mBTC", top + 34)
	write_text("Accept with PIN", top + 43)
	write_text("Wallet " + str(loaded_wid) + " loaded", top + 54)
	return 0

def scrambled_numpad(numbers):
	clear_disp()
	sep = "  "
	line1 = str(numbers[1]) + sep + str(numbers[2]) + sep + str(numbers[3])
	line2 = str(numbers[4]) + sep + str(numbers[5]) + sep + str(numbers[6])
	line3 = str(numbers[7]) + sep + str(numbers[8]) + sep + str(numbers[9])
	line4 = " " + sep + str(numbers[0])
	write_text(line1, top, True)
	write_text(line2, top + 16, True)
	write_text(line3, top + 32, True)
	write_text(line4, top + 48, True)
	return 0