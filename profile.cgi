#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import index
import sessions
import global_settings

# TODO: Organize into different methods


if __name__ == '__main__':
	print 'Content-type: text/html\n'
	DATABASE = global_settings.DATABASE
	msg = ""
	links = "<li><a href='signin.cgi'>SHE Login</a></li>" # default right navbar link is SHE login page
	
	form_data = cgi.FieldStorage()
	if 'timeout' in form_data:
		msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours. Please log in again.</div>"
	
	sessionInfo = sessions.sessionExists()
	if sessionInfo: 
		sessid = sessionInfo[0]
		sess_data = sessionInfo[1]
		if not sessions.checkTimestamp(sessid, sess_data): 
			print "Location: index.cgi?timeout=True"
		else: # if the session is still good, the right navbar link should be for the SHE to answer questions
			links = "<li><a href='answerQuestions.cgi'>Answer Questions</a></li><li><a href='profile.cgi'>Profile</a></li><li><a href='index.cgi?logout=True'>Log Out</a></li>"
	
	tmpl = cgi_utils_sda.file_contents("profile.html") # template
	page = tmpl.format(message=msg, rightLinks=links)
	print page
	
