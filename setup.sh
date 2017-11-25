#!/bin/bash

apt-get -y update;
apt-get -y upgrade;
apt-get -y install python3;
apt-get -y install python3-pip;
pip3 install bs4
pip3 install requests
pip3 install lxml
