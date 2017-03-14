#!/usr/bin/python

# ERROR: mysql.connector not recognized.
# import MySQL.Connector as mariadb
# mariadb_connection = mariadb.connect(user='morse', password='morse', database='morse')
# cursor = mariadb_connection.cursor()

import MySQLdb, sys

# Check that the input arguments are valid.
if len(sys.argv) != 2:
    print "Please input exactly one string.\ne.g.: ./python_DB_test3_set.py Test"
    exit()

input = sys.argv[1]

# Opening a connection to the database.
print "Connecting..."
db_location = "localhost"
db = MySQLdb.connect(host=db_location, user="morse", passwd="morse", db="morse")
print "Connected."

# create a cursor for the select
cur = db.cursor()

# execute an sql query
# cur.execute("SELECT `Character`,`Code` FROM morse.morse")
# cur.execute("SELECT * FROM morse WHERE `Character` IN ('A', 'B')")
character_set = list(set(input.upper()))
query = "SELECT `Character`,`Code` FROM morse WHERE `character` IN ({C})".format(C=str(character_set)[1:-1])
cur.execute(query)

# A perhaps cleaner way that I can't seem to make work.
# placeholders = ','.join('?' * len(l))
# query = "SELECT `code` FROM morse WHERE `character` IN ({P})".format(P=placeholders)
# cur.execute(query, character_set)

# loop to iterate
morse = {}
for row in cur.fetchall() :
    morse[row[0]] = row[1]
    # print row[0] + ": " + morse[row[0]]

# Going through the input
inputUpper = input.upper()
output = ""
for character in inputUpper:
#    print "{x}".format(x=character)
    if character in morse:
        output += morse[character] + " "
    else:
        output += character

print output

# One example query (more serious)
# cur.execute("select * from morse where `Character`='A';")
# code = cur.fetchone()
# print "The character 'A' corresponds to " +code[1]

# close the cursor
cur.close()

# close the connection
db.close ()
