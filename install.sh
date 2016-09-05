#!/bin/bash
apt-get install sudo libssl-dev openssl screen build-essential python3 wget unzip nodejs -y
wget https://github.com/jQwotos/Kissanime-Mass-Downloader/archive/master.zip
unzip master.zip
cd Kissanime*
pip3 install -r requirements.txt
echo "I recommend using screen if you are using SSH to access a remote server, it allows you to run a terminal in the background of the server"
echo "To initialize a screen just type screen"
