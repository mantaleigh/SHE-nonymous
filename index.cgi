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
	page = 1
	links = "<li><a href='signin.cgi'>SHE Login</a></li>" # default right navbar link is SHE login page
	questionCount = index.getCompletedCount(DATABASE)

	form_data = cgi.FieldStorage()
	if 'logout' in form_data:
		sessions.logout()
		msg = "<div class='signin-alert alert alert-success' role='alert'>You have been logged out successfully.</div>"
	if 'timeout' in form_data:
		msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours. Please log in again.</div>"
	if 'page' in form_data: 
		page = cgi.escape(form_data.getfirst('page'))
	
	try: 
		page = int(page)
		qdump = index.getQuestionsPaginated(DATABASE, False, page) # Gets the paginated questions without SHE features
	except ValueError: 
		qdump = "<div class='signin-alert alert alert-danger' role='alert'>{page} is not a valid page. Please correct and try again.</div>".format(page=page)

	next = page + 1
	prev = page - 1
	
	if questionCount <= 10: 
		pagerButtons = ""
	elif page == 1: # show only the next button if the user is at the beginning and there are more than 10 questions
		pagerButtons = "<li><a href='index.cgi?page=" + str(next) + "'>Next</a></li>"
	elif page * 10 >= questionCount and page != 1: # only show the previous button if you're on the last page (and there are multiple pages)
		pagerButtons = "<li><a href='index.cgi?page=" + str(prev) + "'>Previous</a></li>"
	else: 
		pagerButtons = "<li><a href='index.cgi?page=" + str(prev) + "'>Previous</a></li><li><a href='index.cgi?page=" + str(next) + "'>Next</a></li>"

	sessionInfo = sessions.sessionExists()
	if sessionInfo: 
		sessid = sessionInfo[0]
		sess_data = sessionInfo[1]
		if not sessions.checkTimestamp(sessid, sess_data): 
			msg = "<div class='signin-alert alert alert-danger' role='alert'>You have been logged out after 6 hours. Please log in again.</div>"
		else: # if the session is still good, the right navbar link should be for the SHE to answer questions
			links = "<li><a href='answerQuestions.cgi'>Answer Questions</a></li><li><a href='profile.cgi'>Profile</a></li><li><a href='index.cgi?logout=True'>Log Out</a></li>"
			qdump = index.getQuestionsPaginated(DATABASE, True, page) # update the question dump to include SHE features
	
	tmpl = cgi_utils_sda.file_contents("index.html") # template
	page = tmpl.format(allQuestions=qdump, message=msg, rightLinks=links, pagerButtons=pagerButtons)
	print page
	
