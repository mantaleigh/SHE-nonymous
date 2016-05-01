#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/27/16
signin.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect
import cgi_utils_sda as cgi_utils

USER = 'svoigt'

def checkInfo(database, user, passwd): 
	'''
	Checks that the given login information is correct - returns True or False
	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT login_id FROM login WHERE login_id = %s AND passhash = SHA1(%s);"
	curs.execute(statement, (user, passwd))
	row = curs.fetchone()
	return row # return whether or not the log in was successful

