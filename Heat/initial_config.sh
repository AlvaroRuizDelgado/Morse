#!/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
git clone https://github.com/AlvaroRuizDelgado/Morse.git
. Morse/install.sh
. Morse/run_flask
