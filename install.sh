#!/bin/bash

# COMP1203 Setup Script
# Laurie Kirkcaldy / Josh Curry 2018

sudo raspi-config nonint do_spi 0 # enable SPI
sudo raspi-config nonint do_serial 1 # disable linux serial, enable hardware serial
sudo sed -i -e "s/enable_uart=0/enable_uart=1/" /boot/config.txt
cd ~/comp1203-python
git pull
git checkout master
pcmanfm --set-wallpaper /usr/share/rpd-wallpaper/fjord.jpg
echo "Rebooting in 3 seconds. CTRL-C to interrupt."
sleep 3
sudo reboot
