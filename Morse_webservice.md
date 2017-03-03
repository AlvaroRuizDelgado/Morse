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

I'm not being able to access the server I created in the OpenStack machine. The options I see are listed below (note that none would allow for icmp to work).
- VPN.
- OVS bridge configuration.
- SSH port redirection --> most promising, but unsure how to do it.

I had a problem with the security group, I wasn't letting servers access each other (TCP 5000 wasn't allowed).

Check the run.py executable, I'm confused about the naming conventions.

$$
x = 3
$$
