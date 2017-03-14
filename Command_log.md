## Openstack cfg commands

Create a private network.
```bash
neutron net-create morse-net
```

Create an IPv4 subnet on the private network.
```bash
neutron subnet-create --name demo-subnet --ip-version 4 --dns-nameserver 8.8.4.4 morse-net 192.168.0.0/24
```

Create a router.
```bash
neutron router-create router-morse
neutron router-interface-add router-morse morse-subnet
neutron router-gateway-set router-morse public
```

Create the appropriate security group rules.
```bash
openstack security group create morse-sg
openstack security group rule create --proto icmp --dst-port 0 morse-sg
openstack security group rule create --proto tcp --dst-port 22 morse-sg
openstack security group rule create --proto tcp --dst-port 80 morse-sg
openstack security group rule create --proto tcp --dst-port 5000 morse-sg

```

Launch an instance.
```bash
openstack server create --flavor m1.tiny --image $(openstack image list | awk '/Ubuntu/ {print $2}') --nic net-id=$(openstack network list | awk '/ morse-net / {print $2}') --security-group morse-sg --key-name mykey server-01
```

Assign it a floating ip (from an available pool, e.g. public).
```bash
openstack ip floating pool list
openstack ip floating create public
openstack ip floating add x.x.x.x server01
```

## Server cfg commands

Assuming python is pre-installed.
```bash
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get -y install python-virtualenv
mkdir morse
cd morse
virtualenv venv --system-site-package
. venv/bin/activate
pip install Flask
pip install flask-mysql
```
If it says that Flask is already installed, try:
```bash
pip install Flask --upgrade
```

Now we can create a sample python script and place it in the created folder.
```Python
cat > hello_world.py << EOF
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '\nHello, World!\n\n'
EOF
```

And run the server.
```bash
export FLASK_APP=hello_world.py
flask run --host=0.0.0.0
```

Or, from git:
```bash
sudo apt-get install -y git
git clone https://github.com/AlvaroRuizDelgado/Morse.git
cd Morse
. install.sh
. run_flask
```

## HEAT for stack creation

First, install the client in a virtual environment.
```bash
. venv/bin/activate
pip install python-heatclient
```

Then, acquire the HOT file in a controller node (e.g. scp).
```bash
scp test.yaml student-ruiz@openstack:Heat/test.yaml
```

Run the HOT file.
```bash
heat stack-create -f test.yaml heat-test
```

## Ansible for server configuration

To install in Ubuntu, it may be needed to add Ansible's PPA repository.
```bash
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

Alternatively, we can install it in a virtual environment using pip. This option is particularly well suited to situations in which we want to run both heat and ansible from the controller (e.g., to be able to connect them easily).
```bash
. venv/bin/activate
pip install ansible
```

Create an "ansible.cfg" file in the folder where the playbooks are going to be, and edit it to:
- Make ansible check for the hosts file in the same folder.
- Disable host key checks, which require manual input and would slow down the whole process.

```bash
cat <<_EOF_ > ansible.cfg
inventory = hosts
# uncomment this to disable SSH key host checking
host_key_checking = False
_EOF_
```
Create the hosts file:

```bash
[local]
localhost ansible_connection=local

[morse]

[morse:vars]
ansible_ssh_user = ubuntu
ansible_ssh_private_key_file = ~/.ssh/openstack_rsa

[openstack_vms:children]
morse
```

The IP addresses of the nodes to access would be listed below [morse].

When using ansible from a remote machine, we need to create an SSH bastion to be able to channel the individual SSH connections throught the gateway's IP address. In order to do that, we can add this to the .ssh/config file (after any localforward rule we may have):
```bash
## Openstack server BASTION for Ansible ##
Host 192.168.100.*
IdentityFile ~/.ssh/openstack_rsa
ProxyCommand ssh -q -W %h:%p openstack
```

Once that is done, we can retrieve the IP addresses of the servers by running "openstack server list", and add them under [morse] in the hosts file. Then we can run an ansible playbook to configure all the servers listed there:
```bash
ansible-playbook server_config.yaml
```

It's also possible to have ansible automatically retrieve the IPs from openstack through an oficially endorsed file called "openstack.py". However, I think that in order to do this we need to call ansible from the OpenStack controller.

## Database creation.

Load the morse.csv file into MariaDB. As the character ',' is a character used in the database, I changed the commas in the .csv to dollar signs (which are not standardized, and therefore not to be used by me).
```bash
sudo apt-get install -y mariadb-server
mysql -u root -p
CREATE USER morse;
CREATE DATABASE morse;
GRANT ALL PRIVILEGES ON morse.* TO 'morse'@'localhost' IDENTIFIED BY 'morse';
GRANT ALL PRIVILEGES ON morse.* TO 'morse'@'%' IDENTIFIED BY 'morse';
USE morse;
CREATE TABLE morse (
    `Character` VARCHAR(1) CHARACTER SET utf8,
    `Code` VARCHAR(6) CHARACTER SET utf8,
    PRIMARY KEY (`Character`)
);
LOAD DATA LOCAL INFILE "morse.csv" INTO TABLE morse.morse FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n';
```

Installing the mariadb-server through a script instead is a bit tricky, as it would usually ask for the root password. To avoid that we create a non-interactive environment variable to create it without a password, and assign it a password afterwards. In addition, we can put all the sql code into a .sql file and give it to mysql.
```bash
cat <<_EOF_ > install_db.sh
inventory = hosts
# uncomment this to disable SSH key host checking
host_key_checking = False
_EOF_
```

Then we need to install the python connectors for MariaDB.
```bash
. venv/bin/activate
sudo apt-get install python-mysqldb
pip install Flask-MySQLdb
```
