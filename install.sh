#!/bin/bash
sudo apt-get -y install python3-setuptools python3-pyqt5 python3-pip
sudo apt-get -y install build-essential python-dev python-pip
sudo apt-get -y install python-imaging python-smbus
cd dep
sudo pip3 install Electrum-3.1.2.tar.gz
sudo pip3 install RPi.GPIO-0.6.3.tar.gz
sudo pip install RPi.GPIO-0.6.3.tar.gz
python3 -m pip install pyserial-3.4.tar.gz
cd Adafruit_Python_SSD1306-master
sudo python3 setup.py install
cd .. #now in dep
cd .. #now in repo
echo "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
echo "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
echo "||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
echo "-->>> Enable i2c (Option5 -> Option5 -> Yes -> Finish)--<<<"
echo "[Press enter to open wizard and continue]"
read "[Press enter to continue]"
sudo raspi-config
#enable i2c!
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "g_serial" | sudo tee -a /etc/modules
sudo modprobe g_serial
cd core
chmod +x startup.py
echo "[Unit]" > openwallet.service
echo "Description=Openwallet service" >> openwallet.service
echo "After=network.target" >> openwallet.service
echo "" >> openwallet.service
echo "[Service]" >> openwallet.service
echo "ExecStart=/usr/bin/python3 -u startup.py" >> openwallet.service
echo "WorkingDirectory="$(pwd) >> openwallet.service
echo "StandardOutput=inherit" >> openwallet.service
echo "StandardError=inherit" >> openwallet.service
echo "Restart=always" >> openwallet.service
echo "User=pi" >> openwallet.service
echo "" >> openwallet.service
echo "[Install]" >> openwallet.service
echo "WantedBy=multi-user.target" >> openwallet.service
sudo cp openwallet.service /lib/systemd/system/openwallet.service
sudo systemctl enable openwallet.service
cd electrum_fork
SPTH=$(pwd)
export PATH=$PATH:"$SPTH"
cd /usr/bin
sudo ln -s "$SPTH"/elefork
cd ~
source ~/.profile
source ~/.bashrc
echo "Installation finished"