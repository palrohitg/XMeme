#!/bin/bash


# Any installation related commands

sudo apt-get install python3
sudo apt-get install python3-venv
python3 -m venv env
pip3 install -r requirements.txt 


# Installing the Database Dependencies 
curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install mongodb-org
