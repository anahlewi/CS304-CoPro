from __future__ import print_function
import sys
import MySQLdb

def getConn(db):
    '''Connects to a MySQL database using the host information'''
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn
    
def profile(conn, user):
    '''Returns the information to populate the profile page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where user=%s''',[user])
    return curs.fetchone()
    
def dashboard(conn, bnumber):
    '''Returns the information to populate the student's dashboard page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users inner join enrollment using (%s) inner join courses using (%s)''',[bnumber, bnumber])
    return curs.fetchall()
    
def roster(conn, courseNum):
    '''Returns all the students enrolled in a courses'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from enrollment ''') #complicated query tbd
    return curs.fetchall()