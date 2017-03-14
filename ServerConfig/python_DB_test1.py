#!/usr/bin/python 

# ERROR: mysql.connector not recognized.
# import MySQL.Connector as mariadb
# mariadb_connection = mariadb.connect(user='morse', password='morse', database='morse')
# cursor = mariadb_connection.cursor()

import MySQLdb
db = MySQLdb.connect(host="localhost", user="morse", passwd="morse", db="morse")

# create a cursor for the select
cur = db.cursor()

# execute an sql query
cur.execute("SELECT `Character`,`Code` FROM morse.morse")

# loop to iterate
for row in cur.fetchall() :
      #data from rows
      character = str(row[0])
      code = str(row[1])

      #print it
      print character + ": " + code

# One example query (more serious)
cur.execute("select * from morse where `Character`='A';")
code = cur.fetchone()
print "The character 'A' correspons to " +code[0]

# close the cursor
cur.close()

# close the connection
db.close ()
