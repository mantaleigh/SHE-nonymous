#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt

TODO: Documentation
'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import signin
import sessions

VERSION = 'alpha' # the current version of the project (for the session directory)

if __name__ == '__main__':
	my_sess_dir = '/students/svoigt/public_html/cgi-bin/project/' + VERSION + '/SHE-nonymous/sessions/'
	DATABASE = 'svoigt_db'   
	message = ""

	form_data = cgi.FieldStorage()
	if 'submit' in form_data:
		user = cgi.escape(form_data.getfirst('username'))
		passwd = cgi.escape(form_data.getfirst('password'))
		if signin.checkInfo(DATABASE, user, passwd): 
			sessions.start()
			print "Location: index.cgi"
		else: 
			message = "<div class='signin-alert alert alert-danger' role='alert'>Try Again: Incorrect username or password.</div>"
	
	
	print 'Content-type: text/html\n'
	tmpl = cgi_utils_sda.file_contents("signin.html") # template
	page = tmpl.format(msg=message)
	print page


