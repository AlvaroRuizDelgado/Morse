#!/bin/bash

# sudo debconf-set-selections <<< 'mariadb-server mysql-server/root_password password morse'
# sudo debconf-set-selections <<< 'mariadb-server mysql-server/root_password_again password morse'
# sudo apt-get -y install mariadb-server

db_password=morse

export DEBIAN_FRONTEND=noninteractive
sudo -E apt-get -q -y install mariadb-server
unset DEBIAN_FRONTEND
mysqladmin -u root password $db_password

cat morse_db.sql | mysql -u root -p$db_password
