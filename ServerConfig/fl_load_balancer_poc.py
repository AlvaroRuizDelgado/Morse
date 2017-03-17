#!/usr/bin/env python

import os
from flask import Flask,redirect

app = Flask(__name__)

@app.route('/')
def hello():
    # We start the values at 1, because we are going to use the len() function to set the limits in the randint part.
    webservers = {
           1 : "http://www.google.com",
           2 : "http://www.yahoo.com"
    }
    return redirect(webservers[randint(1,len(webservers))])
#    return redirect("http://www.google.com")
#    return redirect("http://192.168.100.205:5000")

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
~
