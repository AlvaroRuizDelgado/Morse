#!/bin/bash

# Update and install
sudo apt update
# sudo apt-get dist-upgrade
sudo apt -y install python-virtualenv

# Create virtual environment and install Flask in it
virtualenv venv --system-site-package
. venv/bin/activate
pip install Flask
# pip install flask-mysql
. run_mogi
