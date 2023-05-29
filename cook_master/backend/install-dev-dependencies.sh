#!/bin/bash

activate () {
  . ../../cook_master-env/bin/activate
}
python3 -m venv ../../cook_master-env

echo -e "\nInstalling dev dependencies..."

activate

sudo apt-get -y update
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo apt-get -y install curl
pip install -r 'dev-requirements.txt'
pip install -r 'requirements.txt'
