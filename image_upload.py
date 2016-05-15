#!/usr/local/bin/python2.7

import os
import sys
import cgi
import re
import MySQLdb

import dbconn
from wendy_dsn import DSN
import cgi_utils_sda

DEST_DIR = '/home/cs304/public_html/images/'
DEST_URL = '/~cs304/images/'
IN_DB    = False                # false means store in dest_dir
MAX_FILE_SIZE = 100000          # 100 KB

# ================================================================

database_connection = None
cursor = None

def cursor():
    global database_connection, cursor
    DSN['database'] = 'wmdb'
    database_connection = dbconn.connect(DSN)
    cursor = database_connection.cursor(MySQLdb.cursors.DictCursor) # results as dictionaries
    return cursor

def generate_actor_menu(cursor):
    '''Returns an HTML menu of all actors in the WMDB'''
    cursor.execute('SELECT nm,name FROM person ORDER BY name')
    menu = '<select name="menu-nm">\n'
    for row in cursor.fetchall():
        menu += '<option value="{nm}">{name} ({nm})</option>\n'.format(
            nm=row['nm'],name=row['name'])
    menu += '</select>\n'
    return menu

def filesize(absfilename):
    '''Returns the length of a file in bytes'''
    stat = os.stat(absfilename)
    return stat.st_size

def check_integer(string,default):
    '''Converts string to an integer if it's all digits, otherwise
returns default'''
    if re.search('^\\d+$',string):
        try:
            return int(string)
        except:
            return default
    else:
        return default

def store_data_in_database(nm,client_filename,file_data,cursor):
    '''inserts or updates picture blob for this actor'''
    try:
        rows_mod = cursor.execute('''
INSERT INTO picblob(nm,pic) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE pic=%s
''',
                                  (nm,file_data,file_data))
    except Exception as e:
        print e
        return 'Failure to store picture data into database: '+str(e)
    if rows_mod != 1:
        return ('Failure to store picture data into database; '+
                'rows modified is '+
                str(rows_mod))
    return 'Successfully uploaded picture data for nm='+str(nm)

def store_data_in_filesystem_optimistic(nm,client_filename,file_data,cursor):
    '''Stores data in the filesystem as nm.jpg without checking for errors'''
    dest_file = DEST_DIR + str(nm) + '.jpg'
    stream = open(dest_file,'wb')
    stream.write(file_data)
    os.chmod(dest_file,0644)
    ## Now, record the URL in the database
    ## inserts or updates picture blob for this actor
    url = DEST_URL + str(nm) + '.jpg'
    rows_mod = cursor.execute('''
INSERT INTO picfile(nm,url) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE url=%s
''',
                              (nm,url,url))
    return ('''
The picture file {fromfile} was uploaded successfully as {tofile}
<a href="{url}"><img src="{url}"></a> '''.format(fromfile=client_filename,
                                           tofile=client_filename,
                                                 url=url))

def store_data_in_filesystem(nm,client_filename,file_data,cursor):
    '''Stores data in the filesystem as nm.jpg in an exception handler'''
    dest_file = DEST_DIR + str(nm) + '.jpg'
    try:
        return store_data_in_filesystem_optimistic(nm,client_filename,file_data,cursor)
    except Exception as e:
        return 'Failure to create output file %s: %s' % (dest_file,e)
    

def store_data_in_filesystem_paranoid(nm,client_filename,file_data,cursor):
    '''Stores data checking for lots of errors'''
    dest_file = DEST_DIR + str(nm) + '.jpg'
    try:
        stream = open(dest_file,'wb')
    except Exception as e:
        return 'Failure to open output file %s: %s' % (dest_file,e)
    try:
        stream.write(file_data)
    except Exception as e:
        return 'Failure to copy file data to %s: %s' % (dest_file,e)
    try:
        os.chmod(dest_file,0644)
    except Exception as e:
        return 'Failure to make file %s world-readable: %s' % (dest_file,e)

    ## Now, record the URL in the database
    url = DEST_URL + str(nm) + '.jpg'
    try:
        ## inserts or updates picture blob for this actor
        rows_mod = cursor.execute('''
INSERT INTO picfile(nm,url) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE url=%s
''',
                                  (nm,url,url))
    except Exception as e:
        print e
        return 'Failure to store picture URL in database: '+str(e)
    if rows_mod != 1:
        return ('Failure to store picture URL in database; '+
                'rows modified is '+
                str(rows_mod))
    return ('The picture file %s was uploaded successfully as %s (%s) ' %
            (client_filename,dest_file,url))


def process_file_upload(actornm,client_filename,local_file,cursor):
    ## Test if the file was uploaded
    if not client_filename:
        return 'No file uploaded (yet)'
        
    file_data = local_file.read()
    ## Double check whether the file upload is too big
    if len(file_data) > MAX_FILE_SIZE:
        return 'Uploaded file is too big: '+str(len(file_data))

    ## Get the nm, which we will either use as a DB key or a filename
    nm = check_integer(actornm,None)
    if nm == None:
        return 'nm has illegal value: %s' % actornm
            
    if IN_DB:
        return store_data_in_database(nm,client_filename,file_data,cursor)
    else:
        return store_data_in_filesystem(nm,client_filename,file_data,cursor)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: %s T/F actornm filename" % sys.argv[0]
        print "First arg says whether to store in the DB (wmdb) as a blob"
        print "T stores in DB, F stores in filesystem"
    else:
        IN_DB = sys.argv[1] == 'T' 
        if IN_DB:
            print 'Storing in database'
        else:
            print 'storing in filesystem'
        actornm = sys.argv[2]
        local_filename = sys.argv[3]
        if filesize(local_filename) > MAX_FILE_SIZE:
            print "File too big"
            sys.exit(1)
        local_file = open(local_filename,'r')
        print process_file_upload(actornm,'client_filename',local_file,cursor())
        
