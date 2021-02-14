
#!/bin/bash


# Any installation related commands

sudo apt-get install python3
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate 
pip install -r requirements.txt

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org-shell



# Any configuration related commands