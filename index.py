#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
index.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect

USER = 'svoigt'

def getQuestions(database): 
	'''
	Returns a list (ul) string of all of the questions in the questions table of the database

	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT DATE_FORMAT(ts, '%W %M %w, %Y') as ts, question, answer FROM questions WHERE status='completed' ORDER BY ts ASC;"
	curs.execute(statement)
	lines = []
	lines.append("<ul class='list-group'>")
	while True:
		row = curs.fetchone()
		if row == None: 
			lines.append("</ul>")
			return "\n".join(lines)
		lines.append("<li class='list-group-item'><span class='question'>{question}</span><br><br><span class='answer'>{ans}</span><br><br><span class='timestamp'>Asked on: {ts}</span>".format(ts=row['ts'], question=row['question'], ans=row['answer']))



