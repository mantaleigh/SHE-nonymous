#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 4/19/16
answerQuestions.cgi
'''

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import answerQuestions as aqs

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    DATABASE = 'svoigt_db'   

    # form_data = cgi.FieldStorage()
    # if 'publish' in form_data:
    #     if 'answer' in form_data: # if a non-empty question was asked 
    #         pass

    questionSelect = aqs.makeQuestionSelect(DATABASE)

    tmpl = cgi_utils_sda.file_contents("answerQuestions.html") # template
    page = tmpl.format(questionSelect=questionSelect)
    print page
    
