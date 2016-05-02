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

def getQuestions(database, loggedIn): 
	'''
	Takes in the current database as a string and a boolean value representing whether or not a SHE is currently logged in. 

	Returns a list (ul) string of all of the questions in the questions table of the database
	If a SHE is logged in, this list features <edit> buttons, otherwise, it is just a simple list

	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT DATE_FORMAT(ts, '%W %M %w, %Y') as ts, question, answer, id FROM questions WHERE status='completed' ORDER BY ts ASC;"
	curs.execute(statement)
	lines = []
	lines.append("<ul class='list-group'>")
	while True:
		row = curs.fetchone()
		if row == None: 
			lines.append("</ul>")
			return "\n".join(lines)
		if loggedIn:
			lines.append("<li class='list-group-item'><span class='question'>{question}</span><br><br><span class='answer'>{ans}</span><br><br><a class='btn btn-primary' href='answerQuestions.cgi?questionSubmit=True&q_selection={id}' role='button'>Edit Answer</a><br><span class='timestamp'>Asked on: {ts}</span>".format(ts=row['ts'], question=row['question'], ans=row['answer'], id=row['id']))
		else:
			lines.append("<li class='list-group-item'><span class='question'>{question}</span><br><br><span class='answer'>{ans}</span><br><br><span class='timestamp'>Asked on: {ts}</span>".format(ts=row['ts'], question=row['question'], ans=row['answer']))



