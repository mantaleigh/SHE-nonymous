#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
answerQuestions.cgi

TODO: Documentation

'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import answerQuestions as aqs
import sessions
import global_settings

if __name__ == '__main__':
	DATABASE = global_settings.DATABASE 
	msg = ""
	form = aqs.makeQuestionSelect(DATABASE)
	form_data = cgi.FieldStorage()
	profileLink = 'profile.cgi?user='

	sessionInfo = sessions.sessionExists()
	if sessionInfo: 
		sessid = sessionInfo[0]
		sess_data = sessionInfo[1]
		username = sess_data['username']
		profileLink += username
		if not sessions.checkTimestamp(sessid, sess_data): 
			print "Location: index.cgi?timeout=True"

		# if the SHE has logged-out
		if 'logout' in form_data:
			sessions.logout()
			# redirect to home page
			print "Location: index.cgi"

		# choosing a question
		if "questionSubmit" in form_data: 
			if "q_selection" in form_data:
				q_id = form_data.getfirst('q_selection')
				form = aqs.makeAnswerForm(DATABASE, q_id) # render the other form
			else: 
				msg = "<div class='signin-alert alert alert-warning' role='alert'>Please select a question.</div>"

		# publishing/saving an answer
		if "publish" in form_data or "save" in form_data:
			q_id = form_data.getfirst('id')
			if "answer" in form_data: # answer is not blank 
				ans = cgi.escape(form_data.getfirst('answer'))
				ans = ans.replace('\n', '<br />')
				if "publish" in form_data:
					aqs.updateAnswer(DATABASE, q_id, ans, "publish")
				elif "save" in form_data:
					aqs.updateAnswer(DATABASE, q_id, ans, "save")
				form = aqs.makeQuestionSelect(DATABASE) # reload all the question content
			else: 
				msg = "<div class='signin-alert alert alert-danger' role='alert'>Answer field must not be left blank.</div>"
				form = aqs.makeAnswerForm(DATABASE, q_id)
	else: 
		print "Location: signin.cgi"

	print 'Content-type: text/html\n'
	tmpl = cgi_utils_sda.file_contents("answerQuestions.html") # template
	page = tmpl.format(profileLink=profileLink,formContent=form, message=msg)
	print page
	
