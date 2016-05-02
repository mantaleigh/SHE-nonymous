#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
answerQuestions.py

TODO: Write a description of the file

TODO: Color in-progress and not-started questions differently
TODO: Count number of unanswered questions and display


'''

import MySQLdb
import dbConnect

USER = 'svoigt'


def makeQuestionSelect(database): 
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT * FROM questions WHERE status='not-started' OR status='in-progress' ORDER BY ts DESC;"
	curs.execute(statement)
	lines = []
	lines.append("<fieldset class='list-group form-group'>")
	count = 0
	while True:
		row = curs.fetchone()
		if row == None: 
			if count > 0: # there were questions to answer
				lines.append("</fieldset>")
				lines.append("<input type='submit' class='btn btn-primary' name=questionSubmit value='Answer Selected Question'>")
				return "\n".join(lines)
			else: 
				return "<p>There are no questions to answer at this time.</p>"
		count+=1
		lines.append("<div style='border:2px solid black;'><input class='list-group-item form-control' type='radio' name='q_selection' value={id}> Question: {question}\n<p>Status: {status}\n<p>Time submitted: {ts}".format(id=row['id'], question=row['question'], status=row['status'], ts=row['ts']))
		if row['status'] == 'in-progress': 
			lines.append("<p>In-Progress Answer: {curr_answer}".format(curr_answer=row['answer']))
		lines.append("</div>")

def makeAnswerForm(database, id): 
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM questions WHERE id=%s"
	curs.execute(statement, id)
	row = curs.fetchone()
	if row: # only one result
		s = "<fieldset class='form-group'>"
		s += "<p>Question: {q}<br><br>".format(q=row['question'])
		s += "<input type=text name='id' value={id} style='display:none'>".format(id=row['id'])
		s += "<label for='answer'>Answer:</label><br>"
		if row['status'] == 'in-progress' or row['status'] == 'completed': # if an answer already exists, complete or not 
			s += "<textarea class='form-control' name='answer' cols='40' rows='5'>{ans}</textarea><br>".format(ans=row['answer'].replace('<br />', '\n'))
		else: 
			s += "<textarea class='form-control' name='answer' cols='40' rows='5'></textarea><br>"
		s += "</fieldset><div class='btn-group' role='group'>"
		s += "<input class='btn btn-primary' type='submit' name='save' value='Save'><input class='btn btn-primary' type='submit' name='publish' value='Publish'></div>"
		return s
	else: 
		return "ERROR: couldn't find selected question in the database" # shouldn't happen


def updateAnswer(database, q_id, answer, update_type): 
	'''
	Adds the provided question to the questions table in the given database. 
	'''
	conn = dbConnect.connect(database, USER)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM questions WHERE id=%s"
	curs.execute(statement, q_id)
	row = curs.fetchone() # only one result
	timestamp = row['ts']
	# timestamp automatically changes on update - so you have to replace it with the old value
	if update_type == 'publish':
		statement = "update questions set status='completed', answer=%s, ts=%s where id=%s"
		# change the status to completed
	if update_type == 'save': 
		statement = "update questions set status='in-progress', answer=%s, ts=%s where id=%s"
		# change the status to in-progress

	curs.execute(statement, (answer, timestamp, q_id))

