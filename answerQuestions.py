#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
answerQuestions.py

TODO: Write a description of the file

TODO: sort by timestamp

'''

import MySQLdb
import dbconn2

USER = 'svoigt'

		
# Select string looks like this: 
'''
<div>
	<p>Question: {question}
	<p>Status: {status}
	<p>Time submitted: {ts}
	-- if there is a partial answer:
	<p>In-Progress Answer: {curr_answer}
	<input type="submit" name={id} value="Select Question">
</div>
'''


def makeQuestionSelect(database): 
	conn = dbConnect(database)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "select * from questions where status='not-started' or status='in-progress';"
	curs.execute(statement)
	lines = []
	while True:
		row = curs.fetchone()
		if row == None: 
			return "\n".join(lines)
		
		lines.append("<div>\n<p>Question: {question}\n<p>Status: {status}\n<p>Time submitted: {ts}".format(question=row['question'], status=row['status'], ts=row['ts']))
		if row['status'] == 'in-progress': 
			lines.append("<p>In-Progress Answer: {curr_answer}".format(curr_answer=row['answer']))
		lines.append("<input type='submit' name={id} value='Select Question'>".format(id=row['id']))		



def answerQuestion(database, q_id): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''

	print "not implemented yet"

	# conn = dbConnect(database)
	# curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	# statement = "insert into questions (question, status) values (%s, 'not-started');"
	# curs.execute(statement, question)
	# print "added question: " + question # is this an XSS vulnerability?



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
