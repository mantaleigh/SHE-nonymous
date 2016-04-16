#!/usr/local/bin/python2.7

import sys

import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import process

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    DATABASE = 'svoigt_db'    
    
