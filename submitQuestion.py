#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
submitQuestion.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect

USER = 'svoigt'

def addQuestion(database, question): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "INSERT INTO questions (question, status) VALUES (%s, 'not-started');"
	curs.execute(statement, question)
	print "added question: " + question # is this an XSS vulnerability?