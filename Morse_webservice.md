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
- [x] Update the program in the Flask Framework
      Needs text field and trigger button.
- [x] Take it down, re-create it.
- [x] Re-create it through HEAT.
- [x] Configure it through Ansible
- [ ] Connect HEAT and Ansible.
- [ ] Add second web-server and load balancer.
- [ ] Provision database node.
- [ ] Modify the python program to use the database.
      I can make a list of characters, grab only those from the database, and map them to a dictionary.
- [ ] Add a Jenkins based test to check that the result can be decoded into the original text.
- [ ] FFS: docker, GitLab, Gerrit

## Miscellaneous stuff happening

- [x] Security group
  - [x] I had a problem with the security group, I wasn't letting servers access each other (TCP 5000 wasn't allowed).

- [ ] Flask
  - [ ] Check the run.py executable, I'm confused about the naming conventions.

- [ ] Heat:
  - [x] The user_data is not executed. I found that it is copied into a folder though --> it was executed, but it was in the root folder (I expected it in the user folder).
  - [ ] If I use "deployment", the user data doesn't run, and the creation remains in progress until it fails due to timeout.
  - [x] When I create a stack through Heat, it always takes a couple of days until I can access it through the ssh tunnel, and then it works correctly --> the problem was in my .ssh/config, or more precisely, in when it is reloaded.
  ```bash
  Channel 13: open failed: connect failed: Connection refused
  ```
    - [x] Closing and opening the terminal application solves the issue, as it loads the .ssh/config file.

- [ ] Ansible
  - [x] SSH bastion setup.
  - [ ] SSH multiplexing.
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
    - [ ] The best option is to make it a service and use the "service" module.

- [ ] SSH
  - [x] I wasn't sure how to access the server I created in the OpenStack machine. The options I saw are listed below (note that none would allow for icmp to work). In the end SSH port redirection is the easiest and the one that has the least impact.
    - VPN.
    - OVS bridge configuration.
    - Configure apache2 with virtual addresses.
    - SSH port redirection --> just add LocalForward in the .ssh/config file.
    - [x] I ended up creating an SSH bastion to access all machines in the server.
  - [ ] LocalForward stops being active, perhaps after adding variables to the .ssh/config file. I need to reboot to enable the functionality. Is it because of screen keeping ssh connections in the background?
    - Whenever I connect through ssh to a server I receive an error message:
    ```bash
    bind: Address already in use
    channel_setup_fwd_listener_tcpip: cannot listen to port: 8080
    ```
  - [ ] I would like a less clunky way to reload the config file, without having to restart the terminal.

$$
x = 3
$$
