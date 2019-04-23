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
    
def profile(conn, name):
    '''Returns the information to populate the profile page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where name like %s''',[name])
    return curs.fetchone()

def addUser(conn, bnumber, name, email, phone):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into users(bnumber, name, email, phone) 
                         values (%s, %s, %s, %s)''',[bnumber, name, email, phone])
    
    
    
def getBnumber(conn, username):
    '''Returns the student's bnumber'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select bnumber from users where username = %s''',[username])
    return curs.fetchone()

def dashboard(conn, bnumber):
    '''Returns the information to populate the student's dashboard page'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select courseNum, courseName, semester from enrollment inner
    join courses using (courseNum) where bnumber = %s''',[bnumber])
    return curs.fetchall()
    
def roster(conn, courseNum):
    '''Returns all the students enrolled in a courses'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from enrollment where courseNum = %s''',[courseNum]) #complicated query tbd
    return curs.fetchall()

def getAssignments(conn, courseNum):
    '''Returns all the assignments from a course'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select psetNum, psetTitle, dueDate from courses where courseNum = %s''', [courseNum])
    return curs.fetchall()
    
if __name__ == '__main__':
    conn = getConn('c9')
    print(profile(conn, "Anah Lewi"))