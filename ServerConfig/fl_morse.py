#!/usr/bin/env python

from flask import Flask, send_file
#from flask_mysqldb import MySQL
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'morse'
app.config['MYSQL_DATABASE_PASSWORD'] = 'morse'
app.config['MYSQL_DATABASE_DB'] = 'morse'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def get_morse(original):
    morse_dict = get_morse_dict(original.encode("utf-8"))

    output = "String to convert:  {o}  --->  ".format(o=original)
    input = original.upper()
    for character in input:
        if character in morse_dict:
            output += morse_dict[character]
        else:
            output += character

    return output

def get_morse_dict(original):
    # Opening a connection to the database with a cursor.
    cur = mysql.connect().cursor()

    # Retrieve only the necessary characters.
    character_set = list(set(original.upper()))
    query = "SELECT `Character`,`Code` FROM morse WHERE `character` IN ({C})".format(C=str(character_set)[1:-1])
    cur.execute(query)

    # Create the dictionary.
    morse_dict = {}
    for row in cur.fetchall() :
        morse_dict[row[0]] = row[1]

    cur.close()

    return morse_dict

@app.route('/')
def index():
    original = "Welcome!"
    return get_morse(original)

@app.route('/<string:original>')
def conversion(original):
    return get_morse(original)

@app.route('/about')
def about():
    about_file = 'about.md'
    return send_file(about_file, mimetype='text/markdown')

@app.errorhandler(500)
def internal_server_error(error):
    unicode_explanation = "At the moment only the basic ASCII character set is implemented. This is in consonance with the most common international morse standard."
    return unicode_explanation

if __name__ == '__main__':
    app.run(host='0.0.0.0')
