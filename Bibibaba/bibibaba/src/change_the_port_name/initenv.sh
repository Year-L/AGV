#!/bin/bash
echo  'KERNEL=="ttyUSB0", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0666", GROUP:="dialout",  SYMLINK+="ydlidar"' >/etc/udev/rules.d/ydlidar.rules

echo  'KERNEL=="ttyUSB1", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="23a3", MODE:="0666", GROUP:="dialout",  SYMLINK+="stm32"' >/etc/udev/rules.d/stm32.rules

echo  'KERNEL=="ttyUSB2", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0666", GROUP:="dialout",  SYMLINK+="wit"' >/etc/udev/rules.d/wit.rules


service udev reload
sleep 2
service udev restart

