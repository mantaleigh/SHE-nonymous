#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import sessions
import global_settings

if __name__ == '__main__':
	DATABASE = global_settings.DATABASE
	msg = ""
	links = "<li><a href='signin.cgi'>SHE Login</a></li>" # default right navbar link is SHE login page
	
	form_data = cgi.FieldStorage()
	if 'user' in form_data: # should be the case
		page_username = form_data.getfirst('user')


	sessionInfo = sessions.sessionExists()
	if sessionInfo: 
		sessid = sessionInfo[0]
		sess_data = sessionInfo[1]
		if not sessions.checkTimestamp(sessid, sess_data): 
			msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours.</div>"
		else: # if the session is still good, the right navbar link should be for the SHE to answer questions and their profile
			links = "<li><a href='answerQuestions.cgi'>Answer Questions</a></li><li><a href='profile.cgi?user="+ sess_data['username'] +"'>Profile</a></li><li><a href='index.cgi?logout=True'>Log Out</a></li>"
	
		if sess_data['username'] == page_username: 
			# they are on their own page and logged in!!!
			msg = "Welcome to your own page! You can edit things here."



	print 'Content-type: text/html\n'
	tmpl = cgi_utils_sda.file_contents("profile.html") # template
	page = tmpl.format(user=page_username, message=msg, rightLinks=links)
	print page
	
