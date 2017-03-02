#!/usr/bin/env python

from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def index():
    morse_dict = {"a":"o-", "b":"-ooo", "c":"-o-o"}
    original = "alvaro"
    
    output = "String to convert:  {o}  --->  ".format(o=original)
    for character in original:
        if character in morse_dict:
            output += morse_dict[character]
        else:
            output += character
    
    return output

@app.route('/<string:original>')
def conversion(original):
    morse_dict = {"a":"o-", "b":"-ooo", "c":"-o-o"}
    
    output = "String to convert:  {o}  --->  ".format(o=original)
    for character in original:
        if character in morse_dict:
            output += morse_dict[character]
        else:
            output += character
    
    return output

@app.route('/about')
def about():
    about_file = 'readme.md'
    return send_file(about_file, mimetype='text/markdown')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
