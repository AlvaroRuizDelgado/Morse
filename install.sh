#!/bin/bash

# Update and install
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get -y install python-virtualenv

# Create folder and 
virtualenv venv
. venv/bin/activate
pip install Flask
