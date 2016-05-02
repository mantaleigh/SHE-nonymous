#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import index
import sessions


if __name__ == '__main__':
	print 'Content-type: text/html\n'
	DATABASE = 'svoigt_db'
	msg = ""
	qdump = index.getQuestions(DATABASE, False) # gets a string for all the questions, without additional SHE features
	links = "<li><a href='signin.cgi'>SHE Login</a></li>" # default right navbar link is SHE login page

	form_data = cgi.FieldStorage()
	if 'logout' in form_data:
		sessions.logout()
		msg = "<div class='signin-alert alert alert-success' role='alert'>You have been logged out successfully.</div>"
	if 'timeout' in form_data:
		msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours. Please log in again.</div>"

	sessionInfo = sessions.sessionExists()
	if sessionInfo: 
		sessid = sessionInfo[0]
		sess_data = sessionInfo[1]
		if not sessions.checkTimestamp(sessid, sess_data): 
			msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours. Please log in again.</div>"
		else: # if the session is still good, the right navbar link should be for the SHE to answer questions
			links = "<li><a href='answerQuestions.cgi'>Answer Questions</a></li><li><a href='index.cgi?logout=True'>Log Out</a></li>"
			qdump = index.getQuestions(DATABASE, True) # update the question dump to include SHE features
	
	tmpl = cgi_utils_sda.file_contents("index.html") # template
	page = tmpl.format(database=DATABASE, allQuestions=qdump, message=msg, rightLinks=links)
	print page
	
