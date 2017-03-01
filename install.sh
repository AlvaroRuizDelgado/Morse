#!/bin/bash

# Update and install
sudo apt-get update
sudo apt-get -y install python-virtualenv

# Create folder and 
mkdir morse
cd morse
virtualenv venv
. venv/bin/activate
pip install Flask

# Create the hello world script.
cat > hello_world.py << EOF
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '\nHello, World!\n\n'
EOF

# Run it
export FLASK_APP=hello_world.py
flask run --host=0.0.0.0
