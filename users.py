#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
signin.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect
import cgi_utils_sda as cgi_utils
import global_settings

USER = global_settings.USER

def checkInfo(database, username, passwd): 
	'''
	Checks that the given login information is correct - returns True or False
	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT login_id FROM login WHERE login_id = %s AND passhash = SHA1(%s);"
	curs.execute(statement, (username, passwd))
	row = curs.fetchone()
	return row # return whether or not the log in was successful


def addUser(database, username, password):
	''' 
	Adds login information to the database for the given username/password

	Returns True if adding the user to the database was successful, false otherwise (username already taken)
	'''
	conn = dbConnect.connect(database, username)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries

	statement = "SELECT login_id FROM login WHERE login_id = %s;"
	curs.execute(statement, username)
	if curs.fetchone(): # username is already taken
		return False

	# if you get to this point, the username is good
	statement = "INSERT INTO login (login_id, passhash) VALUES (%s, SHA1(%s));"
	curs.execute(statement, (username, password))
	return True




