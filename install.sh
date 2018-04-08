sudo apt-get -y install python3-setuptools python3-pyqt5 python3-pip
sudo apt-get install build-essential python-dev python-pip
sudo apt-get install python-imaging python-smbus
cd dep
sudo pip3 install Electrum-3.1.2.tar.gz
sudo pip3 install RPi.GPIO-0.6.3.tar.gz
sudo pip install RPi.GPIO-0.6.3.tar.gz
cd Adafruit_Python_SSD1306-master
sudo python3 setup.py install
cd ..
echo "Please enable i2c..."
sudo raspi-config
#enable i2c!
"dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
"g_serial" | sudo tee -a /etc/modules
modprobe g_serial