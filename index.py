#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
index.py

TODO: Write a description of the file

'''

import MySQLdb
import dbconn2

USER = 'svoigt'

def getQuestions(database): 
	'''
	Returns a list (ul) string of all of the questions in the questions table of the database

	TODO: Select only those questions that have an answer

	'''
	conn = dbConnect(database)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "select id, ts, question from questions;"
	curs.execute(statement)
	lines = []
	lines.append("<ul>")
	while True:
		row = curs.fetchone()
		if row == None: 
			lines.append("</ul>")
			return "\n".join(lines)
		lines.append("<li>ID: {id}, TIMESTAMP: {ts}, QUESTION: {question}".format(**row))



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
#     getQuestions(DATABASE)
