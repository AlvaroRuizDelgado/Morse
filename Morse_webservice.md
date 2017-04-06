# Morse WebServervice


### Ansible set-up
    - Python web app.
    - Database node + web server node —> morse encoder
    - Test is just to decode the morse code and see that it fits.

### Flow

- [x] Test python webservice
    - [x] Python program: mogi_morse.py
    - [x] WSGI
        - [x] Install Flask
        - [x] Hello world example
    - [x] Put it in an Openstack node and access it.
    - [x] Git integration
- [x] Implement the program in the Flask Framework
- [x] Take it down, re-create it.
- [x] Re-create it through HEAT.
- [x] Configure it through Ansible.
  - [x] SSH bastion --> new LocalForward may not work after initialization.
- [x] Modularize HEAT templates, provision a variable number of nodes.
- [x] Modify the flask app to use a database in a dedicated node.
- [x] Provision database node through HEAT/Ansible.
- [x] Connect HEAT and Ansible (dynamic inventory, controller node).
- [ ] Load balancer for the extra web servers.
  - [x] "Manual load balancer"
  - [ ] Openstack LBaaS
    - [ ] Remote dynamic inventory.
- [ ] Sanitize the network situation --> no floating IPs for VMs.
- [ ] Docker
- [ ] Jenkins based test to check that the result can be decoded into the original text.
- [ ] FFS: GitLab, Gerrit

## Miscellanea

- [ ] Security group
  - [x] I had a problem with the security group, I wasn't letting servers access each other (TCP 5000 wasn't allowed).
  - [ ] I'm not sure how to reload the nodes after making changes to the security group. They seem to keep using the old settings. Surely destroying it all and recreating is not a proper solution...

- [ ] Flask
  - [ ] Check the run.py executable, I'm confused about the naming conventions.
  - [ ] How to make a browser read the MD stuff?
  - [ ] Put it all in a proper Flask folder structure.
  - [ ] Add a way to handle the error if a character is not found in the database.

- [ ] Heat:
  - [x] The user_data is not executed. I found that it is copied into a folder though --> it was executed, but it was in the root folder (I expected it in the user folder).
  - [ ] If I use "deployment", the user data doesn't run, and the creation remains in progress until it fails due to timeout.
  - [x] When I create a stack through Heat, it always takes a couple of days until I can access it through the ssh tunnel, and then it works correctly --> the problem was in my .ssh/config, or more precisely, in when it is reloaded.
  ```bash
  Channel 13: open failed: connect failed: Connection refused
  ```
    - [x] Closing and opening the terminal application solves the issue, as it loads the .ssh/config file.
  - [x] Dynamic inventory to hook Ansible.
  - [x] Separate the modules in different files (type: lib/file.yaml).
  - [ ] I'm using an existing key, I should use one prepared in advance in a different folder.
  - [x] Heat doesn't accept .yml, only .yaml!

- [ ] Ansible
  - [ ] Configuration through Ansible.
    - [x] The first time I connect to a server it asks me if I want to add it to the known_servers file. How to avoid that?
          There is a variable in ansible.cfg for this (host_key_checking), setting it to false works. Alternatively, an environment variable can be set (ANSIBLE_HOST_KEY_CHECKING=false).
    - [ ] Change the "package" instances to "apt", and add a check for the OS.
  - [ ] Starting flask through ansible makes it so it finishes when the playbook ends.
    - [x] Difficulties keeping the flask server running after the playbook ends. Tried daemon, but it only works for C programs.
    - [x] Possible circumvention: running it with nohup:
      ```bash
      nohup flask run --host=0.0.0.0 > flask.log 2>&1 &
      ```
          Interesting to note that this won't run in command mode, because nohup needs a shell to start with.
      - [ ] If I'm using nohup, I should check whether it's already running (registry variable). Ignoring the error works in this case, but it's not good practice.
        - [x] I'm killing it if it exists, still can't figure how to check if it's running using shell and a register. If the process is not there, it fails and ends --> ignore_errors: yes.
    - [ ] The best option is to make it a service and use the "service" module.
  - [ ] Openstack.py to retrieve the IPs of the instances created by Heat and add them to hosts. How to continue to Ansible from Heat?
    - [ ] I can make a script that joins both together, as long as they are in the controller.
  - [x] Separate the modules in different files (or folders in this case).
  - [ ] Do pip install --upgrade setuptools before using pip.

- [ ] LBaaS
  - [x] LBaaS v2 not currently installed in our openstack. Even though it was only experimental in Kilo (our version), it seems that the core functions were mostly the same.
  - [ ] Make one by hand to learn.
  - [ ] Configure it in Ocata.

- [ ] SSH
  - [x] I wasn't sure how to access the server I created in the OpenStack machine. The options I saw are listed below (note that none would allow for icmp to work). In the end SSH port redirection is the easiest and the one that has the least impact.
    - VPN.
    - OVS bridge configuration.
    - Configure apache2 with virtual addresses.
    - SSH port redirection --> just add LocalForward in the .ssh/config file.
    - [x] I ended up creating an SSH bastion to access all machines in the server.
  - [x] LocalForward stops being active, perhaps after adding variables to the .ssh/config file. I need to reboot to enable the functionality.
    - Whenever I connect through ssh to a server I receive an error message:
    ```bash
    bind: Address already in use
    channel_setup_fwd_listener_tcpip: cannot listen to port: 8080
    ```
    - Is it because of screen keeping ssh connections in the background?
    - I think it's related to the bastion setup. The localforward rule may try to re-route to those addresses, then the bastion captures them and changes the port to 6080.
      - As the config file is read sequentially, all the LocalForward directives related to the bastion network have to be located before the bastion setup.
      - This works for those LocalForward, but changing those fields later on to address freshly created nodes, or adding extra ones, doesn't work, as those addresses are already assigned to the bastion proxy.
  - [x] SSH bastion setup for Ansible.
  - [ ] SSH multiplexing through ControlMaster. It seems though that it may not be a good idea, as killing the parent ssh connection could take down the whole thing. Should I use it?
  - [ ] I would like a less clunky way to reload the config file, without having to restart the terminal.

- [ ] Test automation --> Jenkins
  - [x] My manual main test consists on running "curl IP:5000" and see that it works.

- [ ] MariaDB
  - [x] Finding the right connector for flask was a bit tricky. In the end the only package needed is flask-mysql, but it needs to install fully (--upgrade option can help).
  - [ ] Not happy with how I'm passing the .csv file to the database, there must be a better way to deal with the presence of ',' as a character in the list. I would like a way to tell MariaDB to take the first character for the first field.

$$
x = 3
$$
