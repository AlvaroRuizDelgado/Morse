#!/bin/bash

# Update and install
sudo apt update
# sudo apt-get dist-upgrade
sudo apt -y install python-virtualenv

# Create folder and
virtualenv venv
. venv/bin/activate
pip install Flask
