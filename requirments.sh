#!/bin/sh

if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root" 
   echo "usage sudo ./requirements.sh "
   exit 1
else
    apt install python3 -y
    pip3 install bs4
    pip3 install requests
    pip3 install subprocess.run
    chmod +x ebay.py
fi