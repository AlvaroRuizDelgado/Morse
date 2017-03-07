#!/bin/bash
echo "user_data initiated"
sudo apt-get update
# cd /home/ubuntu/
# echo "export PS1=\"\t \[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\\$ \"" >> .bash_profile
# sudo apt-get -y dist-upgrade
sudo apt-get -y install git
git clone https://github.com/AlvaroRuizDelgado/Morse.git
cd Morse
. install.sh
. run_flask
echo "user_data finished"
