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
openstack server create --flavor m1.tiny --image $(openstack image list | awk '/Ubuntu/ {print $2}') --nic net-id=$(openstack network list | awk '/ morse / {print $2}') --security-group $(openstack security group list | awk '/morse/ { print $2 }') --key-name mykey server-01
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

If our webserver is only running this application, we may want to redirect all incoming traffic to port 80 to port 5000 (flask's default). If we have multiple cases, or only want the redirection for particular domain names, we can do this using Apache or NginX. For a simple case like this (all traffic in 80 --> 5000) we can modify the iptables:
```bash
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 5000
```

The above command can be disabled by using -D instead of -D.

## Manual Load Balancer

A load balancer can easily be created with flask by redirecting the inputs as in the (under-developed) "fl_load_balancer_poc.py" example. A random number can be generated to decide which webserver to redirect the traffic too. This is the only node that needs to be able to listen to port 80 (for example, configuring the iptables as shown above). This would be installed following the same steps as the web-server, but using the load_balancer flask file instead.

Note that a much better way (for HA, hardware support, and maintainability) is to use the openstack LBaaS, but older versions don't have it (LBaaS v2 became a full feature in liberty).

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
- We can add a line (inventory = hosts) to make ansible check for the hosts file in the given folder. Alternatively, we can pass the path to hosts as a variable (ansible-playbook -i path/to/hosts playbook.yaml), which is safer and more compatible with a dynamic inventory.
- Disable host key checks, which require manual input and would slow down the whole process.

```bash
cat <<_EOF_ > ansible.cfg
[defaults]
# uncomment this to disable SSH key host checking
host_key_checking = False
_EOF_
```
Create the hosts file:

```
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

We can confirm that these IP addresses are correct through a debug function of ansible that allows to see the resulting hostvars.
```bash
ansible -i staging/hosts webservers -m debug -a "var=hostvars[groups['dbservers'][0]].inventory_hostname"
```

Once that is done, we can retrieve the IP addresses of the servers by running "openstack server list", and add them under the corresponding group in the hosts file. Then we can run an ansible playbook to configure all the servers listed there:
```bash
ansible-playbook site.yml
```

It's also possible to have ansible automatically retrieve the IPs from openstack through an oficially endorsed file called "openstack.py". However, I think that in order to do this we need to call ansible from the OpenStack controller.

In order to have that file working we need to install some other python files first.
```bash
. venv/bin/activate
pip install --upgrade setuptools
pip install ansible
pip install os-client-config
pip install shade
# pip install python-novaclient
```

The file can be called simply as ./openstack --list, although it's better to filter the (large) output.
```bash
# List of openstack servers' addresses
./openstack.py --list | jq -r '._meta.hostvars[].ansible_ssh_host'
# List of groups
./openstack.py --list | jq -r '._meta.hostvars[].openstack.metadata.group'
```

Inside the playbook, the IP private and public adresses can be acquired in a similar way as before:
```bash
ansible -i staging/openstack.py webservers -m debug -a "var=hostvars[groups['dbservers'][0]].openstack.private_v4"
ansible -i staging/openstack.py webservers -m debug -a "var=hostvars[groups['dbservers'][0]].openstack.accessIPv4"
```

The way to get the addresses automatically is to create in heat the appropriate groups that are referenced in ansible (webserver_name: default). To run the playbook using this inventory, we need to specify the openstack.py file and the user to connect to the nodes. The user was previously defined in the hosts file, but as we don't use that now we need to pass it in the cli.
```bash
ansible-playbook -u ubuntu -i staging/openstack.py site.yml
```


The file itself can be found here (with interesting examples):
http://docs.catalystcloud.io/tutorials/ansible-openstack-dynamic-inventory.html


##### Pretty-fying ansible

We can follow the regular organization for Ansible, dividing everything into roles. Ansible comes with an easy way to create the directory structure of a role. For example, to create the common role, in the roles directory, we can type:
```bash
ansible-galaxy init common
```



## Database

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

If, instead, we want to install mariadb-server through a script, it gets a bit tricky, as it would usually ask for the root password. To avoid that we create a non-interactive environment variable to create it without a password, and we assign it a password afterwards. In addition, we can put all the sql code into a .sql file and give it to mysql.
```bash
cat <<_EOF_ > install_db.sh
#!/bin/bash

db_password=morse

export DEBIAN_FRONTEND=noninteractive
sudo -E apt-get -q -y install mariadb-server
unset DEBIAN_FRONTEND
mysqladmin -u root password $db_password

cat morse_db.sql | mysql -u root -p$db_password
_EOF_
```

In order to enable remote access we need to comment out the option "bind-address" in the configuration file (/etc/mysql/my.cnf).
```bash
sudo sed -i 's/bind-address\t/#bind-address\t/' /etc/mysql/my.cnf
sudo service mysql restart
```

In the nodes that run the flask server we need to install the python connectors for MariaDB. Flask-mysql links Flask with MariaDB, while python-mysqldb is needed to connect python scripts to MariaDB.
```bash
sudo apt-get install -y python-mysqldb
. venv/bin/activate
pip install flask-mysql
```

Connectivity can be tested through the mariadb-client package.
```bash
sudo apt-get -y install mariadb-client
mysql -u morse -pmorse -h DB_SERVER_IP morse
```
