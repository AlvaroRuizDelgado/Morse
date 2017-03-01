#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def conversion():
    morse_dict = {"a":"o-", "b":"-ooo", "c":"-o-o"}
    pre_morse = "Alvaro"
    print "Morse for: {m}".format(m=pre_morse)
    
    output = "String to convert:  Alvaro  --->  "
    for character in pre_morse:
        if character in morse_dict:
            output += morse_dict[character]
        else:
            output += character
    
    return output

