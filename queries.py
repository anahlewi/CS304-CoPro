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
    
def profile(conn, bnumber):
    '''Returns the information to populate the profile page using bnumber'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where bnumber = %s''',[bnumber])
    return curs.fetchone()


def emailLogin(conn, email, password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where email = %s and password = %s''',[email, password])
    return curs.fetchone()

def google_login(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username from users where email = %s ''',[email])
    return curs.fetchone()
    
def nameLogin(conn, username, password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where username = %s and password = %s''',[username, password])
    return curs.fetchone()
    

def addUser(conn, bnumber, name, email, phone):
    '''Adds new user to database'''
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
    curs.execute('''select * from enrollment E 
    inner join users as U on E.bnumber = U.bnumber
    where courseNum = %s ''',[courseNum]) #complicated query tbd
    return curs.fetchall()

def getAssignments(conn, courseNum, bnumber):
    '''Returns all the assignments from a course'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if isInstructor(conn, bnumber):
        curs.execute('''select pid, psetTitle, dueDate, maxSize from psets 
                    where courseNum = %s''', [courseNum])
    else:
        curs.execute('''select pid, psetTitle, dueDate, maxSize, groupNum from psets 
                    inner join 
                    (select groupNum, pid, courseNum from groups 
                    inner join groupForPset using (groupNum)
                    where bnumber = %s) as table2 using(pid) 
                    where table2.courseNum = %s''', [bnumber, courseNum])
    return curs.fetchall()

def findCourse(conn, courseNum):
    '''Returns all the assignments from a course'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from courses where courseNum = %s''', [courseNum])
    return curs.fetchone()
    
def courses(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from courses''')
    return curs.fetchall()
    
def update(conn, name, email, phone, residence, avail):
    curs = conn.cursor()
    nr = curs.execute('''update users
                    set name = %s, email = %s, phone = %s, resHall = %s, 
                    availability =%s where email like %s''',
                    [name, email, phone, residence, avail,email])
    return nr

def addAssignment(conn, psetNum, psetTitle, dueDate, maxSize, courseNum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into psets(psetNum, psetTitle, dueDate, maxSize,
    courseNum) values (%s, %s, %s, %s, %s)''', 
    [psetNum, psetTitle, dueDate, maxSize, courseNum])
    
def isInstructor(conn, bnumber):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select userType from users where bnumber = %s''', [bnumber])
    dct = curs.fetchone()
    return dct.get('userType') == 'Instructor'
    
    
    
    
    
    
    
if __name__ == '__main__':
    conn = getConn('c9')
    
    
    # print(profile(conn, 'alewi@wellesley.edu'))
    # print(update(conn, "Anah Lewi", 'alewi@wellesley.edu', '3476832433','STONE', 'Monday Morning 8-12'))
    print(roster(conn, 13587))
    print(isInstructor(conn, 'B20800497'))