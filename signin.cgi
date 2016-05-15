#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt

TODO: Documentation
'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import users
import sessions
import global_settings

VERSION = global_settings.VERSION

if __name__ == '__main__':
	my_sess_dir = global_settings.my_sess_dir
	DATABASE = global_settings.DATABASE
	message = ""

	form_data = cgi.FieldStorage()
	if 'submit' in form_data:
		user = cgi.escape(form_data.getfirst('username'))
		passwd = cgi.escape(form_data.getfirst('password'))
		if users.checkInfo(DATABASE, user, passwd): 
			sessions.start(user)
			print "Location: index.cgi"
		else: 
			message = "<div class='signin-alert alert alert-danger' role='alert'>Try Again: Incorrect username or password.</div>"
	
	
	print 'Content-type: text/html\n'
	tmpl = cgi_utils_sda.file_contents("signin.html") # template
	page = tmpl.format(msg=message)
	print page


