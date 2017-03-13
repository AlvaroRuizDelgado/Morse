#!/bin/bash

sudo apt-get install -y mariadb-server
cat morse_db.sql | mysql -u root -p
