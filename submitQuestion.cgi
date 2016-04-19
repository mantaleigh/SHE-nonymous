#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import process

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    DATABASE = 'svoigt_db'   

    form_data = cgi.FieldStorage()
    if 'submit' in form_data:
    	if 'question' in form_data: # if a non-empty question was asked 
    		print "you asked: " + cgi.escape(form_data.getfirst('question'))
    	else: 
    		print "Please ask a question before hitting submit."
    

    tmpl = cgi_utils_sda.file_contents("submitQuestion.html") # template
    page = tmpl.format()
    print page
    
