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
    


    tmpl = cgi_utils_sda.file_contents("index.html") # template
    page = tmpl.format(database=DATABASE)
    print page
    
