#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
submitQuestion.py

TODO: Write a description of the file

'''

import MySQLdb
import dbconn2

USER = 'svoigt'

def addQuestion(database, question): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''
	conn = dbConnect(database)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "insert into questions (question, status) values (%s, 'not-started');"
	curs.execute(statement, question)
	print "added question: " + question # is this an XSS vulnerability?



def dbConnect(database): 
	''' 
	Connects to the provided database using my cnf file and returns the connection
	'''
	dsn = dbconn2.read_cnf('/students/' + USER + '/.my.cnf')
	dsn['db'] = database
	conn = dbconn2.connect(dsn)
	return conn





# # if the script is run as a script, start here
# if __name__ == '__main__':
#     addQuestion()
