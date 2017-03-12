#!/usr/bin/python 

# ERROR: mysql.connector not recognized.
# import MySQL.Connector as mariadb
# mariadb_connection = mariadb.connect(user='morse', password='morse', database='morse')
# cursor = mariadb_connection.cursor()

import MySQLdb, sys

# Check that the input arguments are valid.
if len(sys.argv) != 2:
    print "Please input exactly one string.\ne.g.: mogi_morse.py Test"
    exit()

# Opening a connection to the database.
db = MySQLdb.connect(host="localhost", user="morse", passwd="morse", db="morse")

# create a cursor for the select
cur = db.cursor()

# execute an sql query
cur.execute("SELECT `Character`,`Code` FROM morse.morse")
# cur.execute("SELECT `code` FROM morse WHERE `character` IN ('A','B')")

# loop to iterate
morse = {}
for row in cur.fetchall() :
    morse[row[0]] = row[1]
    # print row[0] + ": " + morse[row[0]]

# Going through the input
input = sys.argv[1].upper()
output = ""
for character in input:
#    print "{x}".format(x=character)
    if character in morse:
        output += morse[character]
    else:
        output += character

print output

# One example query (more serious)
cur.execute("select * from morse where `Character`='A';")
code = cur.fetchone()
print "The character 'A' corresponds to " +code[1]

# close the cursor
cur.close()

# close the connection
db.close ()
