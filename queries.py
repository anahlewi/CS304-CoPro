from __future__ import print_function
import sys
import MySQLdb
import csv

def getConn(db):
    '''Connects to a MySQL database using the host information'''
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db,
                           local_infile = 1)
    conn.autocommit(True)
    return conn
    
def profile(conn, bnumber):
    '''Returns the information to populate the profile page using a bnumber'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where bnumber = %s''',[bnumber])
    return curs.fetchone()


def emailLogin(conn, email):
    '''Returns user information to process login with email/password login'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username, password, name, bnumber from users where email = %s''',[email])
    return curs.fetchone()

def google_login(conn, email):
    '''Returns a username to process google login with provided email address'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username from users where email = %s ''',[email])
    return curs.fetchone()
    
def nameLogin(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username, password, name, bnumber from users where username = %s''',[username])
    return curs.fetchone()
    

def addUser(conn, username, password, bnumber, name, email, phone, userType):
    '''Adds new user to database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into users(username, password, bnumber, name, email, 
                    phone, userType) values (%s, %s, %s, %s, %s, %s, %s)''',
                    [username, password, bnumber, name, email, phone, userType])
    
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
    '''Returns all the information for a given course'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from courses where courseNum = %s''', [courseNum])
    return curs.fetchone()

def coursesStudent(conn, bnumber):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from courses C
    inner join enrollment as E on C.courseNum = E.courseNum 
    where E.bnumber = %s''', [bnumber])
    return curs.fetchall()
    
def allStudents(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users where users.userType = 'student' ''')
    return curs.fetchall()
    
def courses(conn, bnumber):
    '''Returns all courses lead by a particular instructor/or a student is enrolled'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from courses where instructor = %s''', [bnumber])
    return curs.fetchall()
    
def update(conn, bnumber, username, email, phone, residence, avail):
    '''Updates a user's profile'''
    curs = conn.cursor()
    nr = curs.execute('''update users
                    set username = %s, email = %s, phone = %s, resHall = %s, 
                    availability =%s where bnumber = %s''',
                    [username, email, phone, residence, avail, bnumber])
    return nr

def addAssignment(conn, psetNum, psetTitle, dueDate, maxSize, courseNum):
    '''Insert an assignment into the pset table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into psets(pid, psetTitle, dueDate, maxSize,
    courseNum) values (%s, %s, %s, %s, %s)''', 
    [psetNum, psetTitle, dueDate, maxSize, courseNum])

def addGroups(conn, bnumber, groupNum):
    '''Insert a person to a group'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    nr = curs.execute('''insert into groups(groupNum, bnumber) values (%s, %s)''', [groupNum, bnumber])
    return nr 
    
def isInstructor(conn, bnumber):
    '''Checks to see if the user is an instructor or student'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select userType from users where bnumber = %s''', [bnumber])
    dct = curs.fetchone()
    return dct.get('userType') == 'Instructor'
    
    
def getAssignment(conn, pid):
    '''Returns a particular pset with a given pid'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from psets where pid = %s''', [pid])
    return curs.fetchone()

def updatePsets(conn, pid, psetTitle, dueDate, maxSize, courseNum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update psets set pid = %s, psetTitle = %s, dueDate = %s, 
                    maxSize = %s, courseNum= %s where pid = %s''', 
                    [pid, psetTitle, dueDate, maxSize, courseNum, pid])
    
def deleteAssignment(conn, pid):
    '''Deletes a pset from the pset table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''delete from psets where pid=%s''', [pid])
    
def addCourse(conn, courseNum, courseName, instructor, semester):
    '''Insert a new course into the courses table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into courses(courseNum, courseName, instructor, 
    semester) values (%s, %s, %s, %s)''', 
    [courseNum, courseName, instructor, semester])
   
def groups(conn, courseNum, pid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select G.pid, G.groupNum from groups G 
    where G.courseNum = %s and G.pid = %s''', [courseNum, pid])
    return curs.fetchall()

def numGroup(conn, courseNum, pid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select count(*) as numGroups from groups G 
    where G.courseNum = %s and G.pid = %s''', [courseNum, pid])
    return curs.fetchone()

def psetGroup(conn, courseNum, pid, groupNum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select U.name, U.email, U.phone, G.groupNum from groups G 
    inner join courses as C 
    inner join groupForPset as P 
    inner join users as U 
    on P.groupNum = G.groupNum and C.courseNum= G.courseNum and U.bnumber = P.bnumber 
    where G.courseNum = %s and G.pid = %s and G.groupNum = %s''', 
    [courseNum, pid, groupNum])
    return curs.fetchall()

def chatExists(conn, recip1, recip2):
    '''Returns all the groups form for all psets'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(''' select roomkey from chatHistory
    where (sender = %s and recipient = %s) or 
    (sender = %s and recipient = %s) ''', [recip1, recip2, recip2, recip1])
    return curs.fetchone()
    
def findChat(conn, bnumber):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(''' select U.name, C.recipient from chatHistory C
    inner join users as U 
    on C.recipient = U.bnumber
    where C.sender = %s ''', [bnumber])
    return curs.fetchall()
    
def allChats(conn, bnumber):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(''' select U.name, C.recipient, C.sender, C.message from chatHistory C
    inner join users as U 
    on C.sender = U.bnumber
    where C.recipient = %s ''', [bnumber])
    return curs.fetchall()
    
def allGroups(conn):
    '''Returns all the groups form for all psets'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(''' select * from groups''')
    return curs.fetchall()
    
def match(conn, userResHall):
    '''Returns all users who reside in a particular reshall'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(''' select * from users where users.resHall = %s''', [userResHall])
    return curs.fetchall()

def usernameTaken(conn, username):
    '''Checks to see if a username is taken'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select username from users where username = %s''', [username])
    return curs.fetchone()
    

def loadCSV(conn, fullpath):
    '''Load csv users data into the users table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''LOAD DATA LOCAL INFILE %s INTO TABLE users 
                    FIELDS TERMINATED BY "," 
                    LINES TERMINATED BY "\n"
                    (username, bnumber, name, email)''', [fullpath])

def enrollCSV(conn, fullpath, courseNum):
    '''Uses a CSV file to enroll students in a course'''
    with open (fullpath, 'r') as fn:
        read = csv.reader(fn, delimiter = ',')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        for row in read:
            curs.execute('''insert into enrollment(bnumber, courseNum) values (%s, %s)''', [row[1], courseNum])


def checkEnrollment(conn, username, courseNum):
    '''Checks if a username is enrolled in a course'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from users inner join enrollment using (bnumber) 
                    where username = %s and courseNum = %s''', 
                    [username, courseNum])
    return curs.fetchone()
    
def newPassword(conn, password):
    '''Updates an enrolled users password for account login'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update users set password = %s''', 
                    [password])
    
def deleteCourse(conn, courseNum):
    '''Deletes a course from the database and all related assignments'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''delete from courses where courseNum = %s''',[courseNum])
    
if __name__ == '__main__':
    conn = getConn('c9')
    
    # print(allStudents(conn))
    # print(profile(conn, 'alewi@wellesley.edu'))
    # print(update(conn, "Anah Lewi", 'alewi@wellesley.edu', '3476832433','STONE', 'Monday Morning 8-12'))
    # print(roster(conn, 13587))
    # print(isInstructor(conn, 'B20800497'))
    
    # print(psetGroup(conn,13587, 1, 16 ))
    # print(numGroup(conn,13587, 1))
    # print(groups(conn,13587, 1))
    # loadCSV(conn, 'uploads/roster.csv')
