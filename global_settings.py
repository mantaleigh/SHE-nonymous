# file of global setting variables for use throughout the application 



USER = 'svoigt' # user for database
DATABASE = 'svoigt_db' # database to be used
VERSION = 'beta' # current version of the application (to help locate session files)
my_sess_dir = '/students/svoigt/public_html/cgi-bin/project/' + VERSION + '/SHE-nonymous/sessions/'


# code to secure registration for only SHEs (this code will be distributed to them and change every semester)
# TODO: write a program that will change this reg code automatically
# currently a temporary value for proof-of-concept and testing
REG_CODE = '123ABC'