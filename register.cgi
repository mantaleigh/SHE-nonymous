#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt

TODO: Documentation
'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import sessions
import global_settings
import users

my_sess_dir = global_settings.my_sess_dir
DATABASE = global_settings.DATABASE

if __name__ == '__main__':

	message = ""


	form_data = cgi.FieldStorage()
	if 'submit' in form_data:
		reg_code = cgi.escape(form_data.getfirst('registration-code'))
		user = cgi.escape(form_data.getfirst('username'))
		passwd = cgi.escape(form_data.getfirst('password'))
		if reg_code == global_settings.REG_CODE: 
			if users.addUser(DATABASE, user, passwd): # registration was successful
				sessions.start(user)
				print "Location: index.cgi"
			else: 
				print "<div class='signin-alert alert alert-warning' role='alert'>Username is already taken. Please try again.</div>"
		else: 
			message = "<div class='signin-alert alert alert-danger' role='alert'>Incorrect registration code.</div>"

	
	
	print 'Content-type: text/html\n'
	tmpl = cgi_utils_sda.file_contents("register.html") # template
	page = tmpl.format(msg=message)
	print page

