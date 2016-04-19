#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import index


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    DATABASE = 'svoigt_db'   


    qdump = index.getQuestions(DATABASE) # gets a string for all the questions
    tmpl = cgi_utils_sda.file_contents("index.html") # template
    page = tmpl.format(database=DATABASE, allQuestions=qdump)
    print page
    
