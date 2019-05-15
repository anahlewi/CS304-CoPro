import json
import queries 
from flask import (Flask, url_for, redirect, session, render_template, request, flash, send_from_directory, Response, jsonify)
from werkzeug import secure_filename
import random, math
import matching
from datetime import datetime
from flask_login import (UserMixin, login_required, login_user, logout_user, current_user)
from flask_googlelogin import GoogleLogin
import bcrypt


app = Flask(__name__)
import sys, os, random
import imghdr
import MySQLdb

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])


app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['UPLOADS'] = 'uploads'

app.config.update(
    SECRET_KEY='AIzaSyBbtqYZB9aGi4sPmzbKKJvpV2EpcwDY47g',
    GOOGLE_LOGIN_CLIENT_ID='137996221652-06lt05ueh81jt9rtse06idsdgggmoda5.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='lWDlIeZukzElBCdrnhidGoNR',
    GOOGLE_LOGIN_REDIRECT_URI='http://mysql-workshop-alewi.c9users.io:8082/oauth2callback',
    GOOGLE_LOGIN_SCOPES='https://www.googleapis.com/auth/userinfo.email')

googlelogin = GoogleLogin(app)

users = {}

#User Class used for the GOOGLE Authentication part of application
class User(UserMixin):
    '''user class for each user session '''
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')
        self.email = userinfo.get('email')


#grabs user informaton from google 
@googlelogin.user_loader
def get_user(userid):
    '''Returns a userid'''
    return users.get(userid)


#google authentication callback uses keys and google api cloud information to login with google 
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    '''connects to google auth -- third party login '''
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    #uses google token and extra info in session 
    session['logged_in'] =  True
    
    conn = queries.getConn('c9')
    search = queries.google_login(conn, user.email)
    session['username'] = search['username']
    if search:
        return redirect(url_for('profile'))
        
    else:
        return redirect(params.get('next', url_for('newUser')))
        

#allows user to logout and will redirect to homepage
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return index()

#index page will only be displayed if a user is logged in 
@app.route('/')
def index():
    '''Returns template for dashboard if user is logged in'''
    try:
        if session['logged_in']:
            return dashboard()
    except:
        '''Returns the template for the login page'''
        googleUrl =  googlelogin.login_url(approval_prompt='force')
        return render_template('base.html', url = googleUrl)
        
        
        
@app.route('/dashboard')
def dashboard():
    '''Returns dashboard template'''
    if session['logged_in']:
        return render_template('dashboard.html', name = session['name'], logged_in = session['logged_in'])
    else:
        flash('Need to login to access page')
        return(request.referrer)
    
    
#originally only created a google login page     
@app.route('/manualLogin', methods = ['POST'])
def flaskLogin():
    '''Manual login for users who are already signed up'''
    conn = queries.getConn('c9')
    check = ''
    pwrd = request.form['password']
    print(pwrd)
    if '@' in request.form['username-email']:
        email = request.form['username-email']
        check = queries.emailLogin(conn, email) 
    else:
        username =  request.form['username-email']
        check = queries.nameLogin(conn, username)
    if not check:
       flash('Username/email is not found in the database. Create an account to continue.')
       return redirect(request.referrer)
    else:
        hashed = check['password']
        if bcrypt.hashpw(pwrd.encode('utf-8'), hashed.encode('utf-8')) != hashed:
            flash('Incorrect password')
            return redirect(request.referrer)
        session['logged_in'] =  True
        session['bnumber'] = check['bnumber']   
        session['username'] = check['username']
        session['name'] = check['name']
        return redirect(url_for('profile', bnumber = session['bnumber']))


#Profile page allows user to access their information and other students information
@app.route('/profile')   
@app.route('/profile/')  
@app.route('/profile/<bnumber>')
def profile(bnumber = None):
    '''Renders a user's profile and allow users to access other student's profile'''
    conn = queries.getConn('c9')
    if session.get('logged_in'):
        if bnumber:
            
            userInfo = queries.profile(conn, bnumber)
        else:
            '''if no bnumber is given redirect to current users information
            redirect if users input URL /profile or /profile/ --> no bnumber given '''
            return redirect(url_for('profile', bnumber = session['bnumber']))
    else:
        flash('Need to login to access page')
        return index()
    if bnumber == session['bnumber']:
        currentUser = True
    else:
        currentUser = False 
    return render_template('profile.html', user=userInfo, currentUser = currentUser, logged_in = session['logged_in'])
    
    
#will be redirected to this url when your name is not in database
@app.route('/newUser', methods = ['GET','POST'])
def newUser():
    '''Returns a template for user sign up if the user is not found in the database'''
    if request.method == 'GET':
        return render_template('newUser.html')
    else:
        conn = queries.getConn('c9')
        username = request.form.get('username')
        password = request.form.get('password1')
        password2 = request.form.get('password2')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bnumber = request.form.get('bnumber')
        userType = request.form.get('userType')
        print('queries', queries.usernameTaken(conn, username))
        if queries.usernameTaken(conn, username):
            flash('Username taken. Enter a new username')
            return render_template('newUser.html')
        if password != password2:
            flash('Passwords do not match')
            return render_template('newUser.html')
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if (username and hashed and name and email and phone and bnumber 
        and userType):
            queries.addUser(conn, username, hashed, bnumber, name, email, phone,
            userType)
            flash('Your account has been created. You can go ahead and login!')
            return redirect(url_for('index'))

@app.route('/courses/<courseNum>')
@app.route('/courses')
def courses(courseNum = None):
    '''Display courses student is in enrolled in or courses professor teaches'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        bnumber = session.get('bnumber')
        instructor = queries.isInstructor(conn, bnumber)
        if courseNum:
            course = queries.findCourse(conn, courseNum)
            roster = queries.roster(conn, courseNum)
            session['courseNum'] = courseNum
            students = queries.allStudents(conn)
            psets = queries.getAssignments(conn, courseNum, bnumber)
            
            return render_template('roster.html', course = course, courseNum = courseNum, 
                                    roster = roster, psets = psets, students = students,
                                    logged_in = session['logged_in'], instructor = instructor)
                
        else:
            if instructor:
                courses = queries.courses(conn, bnumber)
            else:
                courses = queries.coursesStudent(conn, bnumber)
            return render_template('courses.html', courses = courses, 
            logged_in = session['logged_in'], instructor=instructor)
    else:
        flash('Need to login to access page')
        return index()
        
@app.route('/updateRoster', methods=['POST'])
def updateRoster():
    conn = queries.getConn('c9')
    bnumber = request.form.get('students')
    courseNum = session.get('courseNum')
    # courseNum = request.form.get('courseNum') # not necessary
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into enrollment(bnumber, courseNum)
                values(%s, %s)''',[bnumber, courseNum])
    return redirect(request.referrer)


@app.route('/rosterUpload', methods=['POST'])
def updateRosterWithUpload():
    file = request.files['roster-csv']
    if not file.filename:
        flash('No file selected')
        return request.referrer
    filename = secure_filename(file.filename)
    if filename.split('.')[-1] in ALLOWED_EXTENSIONS:
        fullpath = os.path.join(app.config['UPLOADS'], filename)
        file.save(os.path.join(app.config['UPLOADS'], filename))
        conn = queries.getConn('c9')
        queries.loadCSV(conn, fullpath)
        courseNum = session.get('courseNum')
        queries.enrollCSV(conn, fullpath, courseNum)
        return redirect(request.referrer)
    else:
        flash('The provided file extension is not allowed for uploads.')
    return None
    
@app.route('/update', methods =['POST'])
def update():
    '''Updates information about current_user'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        username = request.form.get('username')
        print(username)
        email = request.form.get('email')
        phone = request.form.get('phone')
        bnumber = request.form.get('bnumber')
        residence = request.form.get('residence')
        avail= request.form.get('availability')
        print(avail)
        
        try:
            updated = queries.update(conn, bnumber, username, email, phone, residence, avail)
            print(updated)
        except:
            flash('Unable to Update info')
        return redirect(url_for('profile'))
    else:
        return redirect(request.referrer)



@app.route('/api/addexpense')
@login_required
def api_addexpense():
    req = request.get_json()
    return req
    
    
@app.route('/availabilityAjax/', methods=['GET'])
def availabilityAjax():
    '''Waits for changes in availability section to update in the database
        AUTOSAVE FEATURE    
    '''
    
    availability = request.args.get('availability')
    bnumber = request.args.get('bnumber')
    try:
        conn = queries.getConn('c9')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        numrows = curs.execute('''update users set availability = %s
                    where bnumber = %s''', [availability, bnumber])
                    
        
        return jsonify( {'error': False, 'availability': availability, 'bnumber': bnumber} )
    except Exception as err:
        return jsonify( {'error': True, 'err': str(err) } )



@app.route('/algorithmAjax', methods=['GET'])
def match():
    
    '''CRUX OF APPLICATION
        Not a sophisticated algorithm but matches students in the roster
    '''
    courseNum = request.args.get('courseNum')
    pid = request.args.get('pid')
    try:
        conn = queries.getConn('c9')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        roster = queries.roster(conn, courseNum)
        matches = matching.match(roster)
        for match in matches:
            
            allGroups = queries.allGroups(conn)
            groupNum = matching.groupNum(allGroups)
            check = curs.execute('''insert into groups(groupNum, pid, courseNum)
            values(%s, %s, %s)''',[groupNum, pid, courseNum])
            curs.execute('''insert into groupForPset(groupNum, bnumber)
            values(%s, %s)''',[groupNum, match])
        
            if matches[match]:
                curs.execute('''insert into groupForPset(groupNum, bnumber)
                values(%s, %s)''',[groupNum, matches[match]])
        jsonify( {'error': False, 'match': matches })
        return redirect(request.referrer)
    except Exception as err:
        return jsonify( {'error': True, 'err': str(err) } )


@app.route('/pic/<bnumber>')
def pic(bnumber):
    '''URL that displays images of users from uploads folder'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        numrows = curs.execute('''select bnumber,filename from users inner join picfile using (bnumber)
                        where bnumber = %s''', [bnumber])
        if numrows == 0:
            flash('No picture for {}'.format(bnumber))
            return redirect(url_for('profile'))
        row = curs.fetchone()
        val = send_from_directory(app.config['UPLOADS'],row['filename'])
        return val
    else:
        flash('Need to login to access page')
        return index()

@app.route('/course/<courseNum>/group/<pid>/<groupNum>', methods=['GET'])
def group(courseNum, groupNum, pid):
    '''Returns group page for student users'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        course = queries.findCourse(conn, courseNum)
        group = queries.psetGroup(conn, courseNum, pid, groupNum)
    
        return render_template('groups.html', course = course,
        groupNum = groupNum, group = group, logged_in = session['logged_in'])
    else:
        flash('Need to login to access page')
        return index()


@app.route('/course/<courseNum>/groups/<pid>', methods=['GET'])
def groupProf(courseNum, pid):
    '''Returns group page for users that are professors'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        course = queries.findCourse(conn, courseNum)
        groups = queries.groups(conn, courseNum, pid)
        numGroups = queries.numGroup(conn, courseNum, pid)
        return render_template('groupProf.html', course = course, courseNum = courseNum, pid = pid,
        numGroups = numGroups['numGroups'], groups = groups, logged_in = session['logged_in'])
    else:
        flash('Need to login to access page')
        return index()
    
@app.route('/uploadAjax/', methods=["POST"])
def file_upload():
    '''Image upload that uses AJAX to upload image into picfile database'''
    try:
        bnumber = request.form.get('bnumber')
        print(bnumber)# may throw error
        f = request.files['pic']
        print(f)
        mime_type = imghdr.what(f)
        print(mime_type)
        if mime_type.lower() not in ['jpeg','gif','png']:
            raise Exception('Not a JPEG, GIF or PNG: {}'.format(mime_type))
        filename = secure_filename('{}.{}'.format(bnumber,mime_type))
        pathname = os.path.join(app.config['UPLOADS'],filename)
        f.save(pathname)
        conn = queries.getConn('c9')
        curs = conn.cursor()
        curs.execute('''insert into picfile(bnumber,filename) values (%s,%s)
                            on duplicate key update filename = %s''',
                         [bnumber, filename, filename])
        return jsonify( {'error': False, 'image':filename} )
    except Exception as err:
        return jsonify( {'error': True, 'err': err})
        

@app.route('/newAssignment', methods=['GET','POST'])
def newAssignment():
    '''Allows professor to add a new assignment to the database'''
    if session.get('logged_in'):
        if request.method == 'GET':
            return render_template('assignment.html')
        else:
            psetNum = request.form.get('psetNum')
            psetTitle = request.form.get('psetTitle')
            dueDate = request.form.get('dueDate').encode('utf-8')
            maxSize = request.form.get('maxSize')
            conn = queries.getConn('c9')
            courseNum  = session.get('courseNum')
            print('dueDate String', dueDate)
            if psetNum:
                try:
                    psetNum = int(psetNum)
                except:
                    flash('Invalid input: Please insert')
            else:
                flash('Missing input: Assignment Number is missing')
            if not dueDate:
                flash('Missing input: Assignment Duedate is missing')
            if not psetTitle:
                flash('Missing input: Assignment Title is missing')
            if maxSize:
                try:
                    maxSize = int(maxSize)
                except:
                    flash('Invalid input: Please insert an integer')
                    
            print('number', psetNum)
            print('title', psetTitle)
            print('dueDate', dueDate)
            print('maxSize', maxSize)
            if psetNum and psetTitle and dueDate and isinstance(maxSize, int):
                queries.addAssignment(conn, psetNum, psetTitle, dueDate, maxSize, courseNum)
                return redirect(url_for('courses', courseNum = courseNum))
                
            return render_template('assignment.html', logged_in = session['logged_in'])
            
    else:
        flash('Need to login to access page')
        return index()
        
@app.route('/update/<pid>', methods = ['GET', 'POST'])
def deleteAssignment(pid):
    '''Allows professor to deleta assignment and will update database accordingly'''
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        courseNum = session.get('courseNum')
        bnumber = session.get('bnumber')
        instructor = queries.isInstructor(conn, bnumber)
        if request.method == 'GET':
            info = queries.getAssignment(conn, pid)
            return render_template('update.html', pset = info, courseNum = courseNum)
        else:
            if request.form.get('submit') == 'update':
                newPid = request.form.get('pid')
                psetTitle = request.form.get('psetTitle')
                dueDate = request.form.get('dueDate')
                maxSize = request.form.get('maxSize')
                queries.updatePsets(conn, newPid, psetTitle, dueDate, maxSize, courseNum)
                return redirect(url_for('courses', courseNum = courseNum, instructor = instructor))
                
            elif request.form.get('submit') == 'delete':
                queries.deleteAssignment(conn, pid)
        return redirect(url_for('courses', courseNum=courseNum, instructor=instructor))
    else:
        flash('Need to login to access page')
        return index()

@app.route('/newCourse', methods=['GET', 'POST'])
def newCourse():
    '''Allows professors to add new course to database and will be displayed on courses page'''
    if session.get('logged_in'):
        bnumber = session.get('bnumber')
        if request.method == 'GET':
            return render_template('newCourse.html', bnumber = bnumber)
        else:
            courseNum = request.form.get('courseNum')
            courseName = request.form.get('courseName')
            semester = request.form.get('semester')
            if courseNum:
                try:
                    courseNum = int(courseNum)
                except:
                    flash('Invalid input: Please enter integer values')
            else:
                flash('Missing input: Course Number is missing')
                
            if not courseName:
                flash('Missing input: Course Title is missing')
            if not semester:
                flash('Missing input: Semester is missing')
                
            if isinstance(courseNum, int) and courseName and semester:
                conn = queries.getConn('c9')
                queries.addCourse(conn, courseNum, courseName, bnumber, semester)
                return redirect(url_for('courses'))
        return render_template('newCourse.html', bnumber = bnumber, logged_in = session['logged_in'])
    else:
        flash('Need to login to access page')
        return index()

@app.route('/deleteCourse')
def deleteCourse(courseNum):
    conn = queries.getConn('c9')
    queries.deleteCourse(conn, courseNum)
    return redirect("url_for('courses')")
    
    
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
