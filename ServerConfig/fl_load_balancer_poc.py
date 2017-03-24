#!/usr/bin/env python

import os, random
from flask import Flask,redirect

app = Flask(__name__)

@app.route('/')
def hello():
    # We start the values at 1, because we are going to use the len() function to set the limits in the randint part.

    # No need to import random
    # webservers = {
    #        1 : "http://www.google.com",
    #        2 : "http://www.yahoo.com"
    # }
    # return redirect(webservers[randint(1,len(webservers))])

    # Importing random
    webservers = [
           "http://www.google.com",
           "http://www.yahoo.com"
    ]
    return redirect(random.choice(webservers))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
~
