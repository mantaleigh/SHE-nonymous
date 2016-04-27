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
    form = aqs.makeQuestionSelect(DATABASE)
    form_data = cgi.FieldStorage()

    # choosing a question
    if "questionSubmit" in form_data: 
        if "q_selection" in form_data:
            q_id = form_data.getfirst('q_selection')
            form = aqs.makeAnswerForm(DATABASE, q_id) # render the other form
        else: 
            print "please select a question."

    # publishing/saving an answer
    if "publish" in form_data or "save" in form_data:
        if "answer" in form_data: # answer is not blank 
            ans = cgi.escape(form_data.getfirst('answer'))
            ans = ans.replace('\n', '<br />')
            q_id = form_data.getfirst('id')
            if "publish" in form_data:
                aqs.updateAnswer(DATABASE, q_id, ans, "publish")
            elif "save" in form_data:
                aqs.updateAnswer(DATABASE, q_id, ans, "save")
            form = aqs.makeQuestionSelect(DATABASE) # reload all the question content
        else: 
            print "Answer field must not be left blank"




    tmpl = cgi_utils_sda.file_contents("answerQuestions.html") # template
    page = tmpl.format(formContent=form)
    print page
    
