#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
submitQuestion.cgi

TODO: Documentation

'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import submitQuestion as sq
import sessions
import global_settings

if __name__ == '__main__':
    DATABASE = global_settings.DATABASE  
    links = "<li><a href='signin.cgi'>SHE Login</a></li>" # default right navbar link is SHE login page
    msg = ""

    form_data = cgi.FieldStorage()

    sessionInfo = sessions.sessionExists()
    if sessionInfo: 
        sessid = sessionInfo[0]
        sess_data = sessionInfo[1]
        if not sessions.checkTimestamp(sessid, sess_data): 
            print "Location: index.cgi?timeout=True"
        else: # if the session is still good, the right navbar link should be for the SHE to answer questions
            links = "<li><a href='answerQuestions.cgi'>Answer Questions</a></li><li><a href='profile.cgi?user="+ sess_data['username'] +"'>Profile</a></li><li><a href='index.cgi?logout=True'>Log Out</a></li>"

    # if the SHE has logged-out
    if 'logout' in form_data:
        sessions.logout()
        # redirect to home page
        print "Location: index.cgi"

    if 'submit' in form_data:
    	if 'question' in form_data: # if a non-empty question was asked 
            ques = cgi.escape(form_data.getfirst('question'))
            ques = ques.replace('\n', '<br />')
            sq.addQuestion(DATABASE, ques)
            msg = "<div class='signin-alert alert alert-success' role='alert'>Thank you! Your question has been submitted successfully.</div>"
    	else: 
    		msg = "<div class='signin-alert alert alert-warning' role='alert'>Please ask a question before hitting submit.</div>"
    

    print 'Content-type: text/html\n'
    tmpl = cgi_utils_sda.file_contents("submitQuestion.html") # template
    page = tmpl.format(rightLinks=links, message=msg)
    print page
    
