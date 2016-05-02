#!/usr/local/bin/python2.7

'''
Author: Samantha Voigt
Last Modified: 5/1/16

Module for creating, deleting, and interacting with sessions having to deal with SHE login.

'''

# TODO: Change minutes=X to hours=6 once testing is over.


import os
import pickle
import cgi_utils_sda
import datetime

VERSION = 'alpha'
my_sess_dir = '/students/svoigt/public_html/cgi-bin/project/' + VERSION + '/SHE-nonymous/sessions/'

def sessionExists(): 
	'''
	If there is (SHE) session data for the current user, return the the session id and the session data in a tuple. 
	Otherwise, return False.
	'''
	sessid = cgi_utils_sda.session_id()
	# check to see if there's any session data for this session id
	if os.path.isfile(my_sess_dir+sessid):
		input = open(my_sess_dir+sessid,'r')
		sess_data = pickle.load(input)
		input.close()
		if isinstance(sess_data,dict):
			return (sessid, sess_data)
	else:
		return False

def start(): 
	'''
	Starts a new session by creating a file with the current timestamp in the session data.
	'''
	sess_data = cgi_utils_sda.session_start(my_sess_dir)
	sess_data['timestamp'] = datetime.datetime.now()
	cgi_utils_sda.save_session(my_sess_dir,sess_data)

def checkTimestamp(sessid, sess_data): 
	'''
	Takes in as parameters the session id and the session data for the session to check the timestamp of. 

	If the timestamp of the session is greater than 6 hours, then delete the session entirely, forcing the SHE to log back in. 
	Otherwise, let them continue by doing nothing. Returns True if the session is still good, False if the session needed to be deleted.
	'''
	now = datetime.datetime.now()
	delta = now - sess_data['timestamp']
	if delta > datetime.timedelta(minutes=5):
		os.remove(my_sess_dir+sessid)
		return False
	else: 
		return True

def logout(): 
	'''
	Deletes the session file associated with the current session if it exists.
	'''
	sessid = cgi_utils_sda.session_id()
	if os.path.isfile(my_sess_dir+sessid):
		os.remove(my_sess_dir+sessid)




