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
- [ ] Re-create it through HEAT.
- [ ] Configure it through Ansible
- [ ] Make morse database.
- [ ] Update HEAT and Ansible templates.
- [ ] Modify the python program to use the database.
      I can make a list of characters, grab only those from the database, and map them to a dictionary.
- [ ] Update it through Ansible.
- [ ] Add a Jenkins based test to check that the result can be decoded into the original text.
- [ ] FFS: docker

## Miscellaneous stuff happening

- [x] I wasn't sure how to access the server I created in the OpenStack machine. The options I saw are listed below (note that none would allow for icmp to work). In the end SSH port redirection is the easiest and the one that has the least impact.
    - VPN.
    - OVS bridge configuration.
    - SSH port redirection --> just add LocalForward in the .ssh/config file.
    - Configure apache2 with virtual addresses.
- [x] I had a problem with the security group, I wasn't letting servers access each other (TCP 5000 wasn't allowed).
- [ ] Check the run.py executable, I'm confused about the naming conventions.
- [ ] When I create a stack through Heat, it always takes a couple of days until I can use the functionality, and then it works correctly.
- [ ] When creating a stack through Heat, I sometimes get a situation in which the ssh tunnel doesn't work, and all I get is an empty reply from server.
```bash
Channel 13: open failed: connect failed: Connection refused
```


$$
x = 3
$$
