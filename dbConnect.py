#!/usr/local/bin/python2.7

# Author: Samantha Voigt
# Module used just for the a method that helps connect to the database

import dbconn2

def connect(database, user): 
	''' 
	Connects to the provided database using my cnf file and returns the connection
	'''
	dsn = dbconn2.read_cnf('/students/' + user + '/.my.cnf')
	dsn['db'] = database
	conn = dbconn2.connect(dsn)
	return conn