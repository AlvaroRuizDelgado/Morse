#!/bin/bash

# Update and install
sudo apt update
# sudo apt-get dist-upgrade
sudo apt -y install python-virtualenv

# Create virtual environment and install Flask in it
virtualenv venv
. venv/bin/activate
pip install Flask
