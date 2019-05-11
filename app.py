import json
import queries 
from flask import (Flask, url_for, redirect, session, render_template, request, flash, send_from_directory, Response, jsonify)
from werkzeug import secure_filename
import random, math
import matching
from datetime import datetime
from flask_login import (UserMixin, login_required, login_user, logout_user, current_user)
from flask_googlelogin import GoogleLogin

app = Flask(__name__)
import sys, os, random
import imghdr
import MySQLdb

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
#url build so that the user comes first then build off ie mhardy2/course/assignments

#user class for each user session 
class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')
        self.email = userinfo.get('email')


@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)

  
   
#connects to google auth -- third party login 
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
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
        

#allows user to logout for testing purpose --> more sophisticated logout will be created    
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return """
        <p>Logged out</p>
        <p><a href="/">Return to /</a></p>
        """

#shows index page and allows people to login
@app.route('/')
def index():
    googleUrl =  googlelogin.login_url(approval_prompt='force')
    return render_template('base.html', url = googleUrl)


#manual login (users were manually added)
@app.route('/manualLogin', methods = ['POST'])
def flaskLogin():
    conn = queries.getConn('c9')
    check = ''
    pwrd = request.form['password']
    if '@' in request.form['username-email']:
        email = request.form['username-email']
        check = queries.emailLogin(conn, email, pwrd) 
    else:
        username =  request.form['username-email']
        check = queries.nameLogin(conn, username, pwrd)
    if not check:
       flash('Incorrect username or password')
       return redirect(request.referrer)
    session['logged_in'] =  True
    session['bnumber'] = check['bnumber']   
    session['username'] = check['username']
    return redirect(url_for('profile', bnumber = session['bnumber']))


#Profile page allows user to access their information and other students information
@app.route('/profile')   
@app.route('/profile/')  
@app.route('/profile/<bnumber>')
def profile(bnumber = None):
    conn = queries.getConn('c9')
    #checks to see if user is logged into a session, otherwise will not be able to acesss
    if session.get('logged_in'):
        if bnumber:
            
            userInfo = queries.profile(conn, bnumber)
        else:
            #if no bnumber is given redirect to current users information 
            #using redirect if users input URL /profile or /profile/ --> no bnumber given 
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
    conn = queries.getConn('c9')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bnumber = request.form.get('bnumber')
        if len(bnumber) == 0:
            flash('enter a bnumber')
        else:
            queries.addUser(conn, bnumber, name, email, phone)
            return redirect(url_for('profile'))
    else:
        name = current_user.name 
        email = current_user.email 
        return render_template('newUser.html', name = name, email = email)
        
@app.route('/courses/<courseNum>')
@app.route('/courses')
def courses(courseNum = None):
    conn = queries.getConn('c9')
    bnumber = session.get('bnumber')
    instructor = queries.isInstructor(conn, bnumber)
    if courseNum:
        course = queries.findCourse(conn, courseNum)
        roster = queries.roster(conn, courseNum)
        session['courseNum'] = courseNum
        
        psets = queries.getAssignments(conn, courseNum, bnumber)
        
        return render_template('roster.html', course = course, courseNum = courseNum, 
                                roster = roster, psets = psets, 
                                logged_in = session['logged_in'], instructor = instructor)
            
    else:
        courses = queries.courses(conn)
        return render_template('courses.html', courses = courses, 
        logged_in = session['logged_in'], instructor=instructor)

    
@app.route('/update', methods =['POST'])
def update():
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

#only works for gauth    
@app.route('/home')
def home():
    return """
        <p>Hello, %s</p>
        <p><img src="%s" width="100" height="100"></p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, current_user.picture)


@app.route('/api/addexpense')
@login_required
def api_addexpense():
    req = request.get_json()
    return req
    
    
@app.route('/availabilityAjax/', methods=['GET'])
def availabilityAjax():
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



@app.route('/algorithmAjax', methods=['POST'])
def match():
    courseNum = request.args.get('courseNum')
    
    try:
        conn = queries.getConn('c9')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        roster = queries.roster(conn, courseNum)
        allGroups = queries.allGroups(conn)
        groupNum = matching.groupNum(allGroups)
        check = curs.execute('''insert into groups(groupNum, pid, courseNum)
        values(%s, %s, %s)''',[groupNum, pid])
    except Exception as err:
        return jsonify( {'error': True, 'err': str(err) } )
        


@app.route('/pic/<bnumber>')
def pic(bnumber):
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


@app.route('/pics/')
def pics():
    conn = queries.getConn('c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select bnumber,filename from picfile inner join users using (bnumber)')
    pics = curs.fetchall()
    return render_template('all_pics.html',pics=pics)


@app.route('/course/<courseNum>/group/<pid>/<groupNum>', methods=['GET'])
def group(courseNum, groupNum, pid):
    conn = queries.getConn('c9')
    course = queries.findCourse(conn, courseNum)
    group = queries.groups(conn, courseNum, pid)
    return render_template('groups.html', course = course,
    groupNum = groupNum, group = group, logged_in = session['logged_in'])


@app.route('/course/<courseNum>/groups/<pid>', methods=['GET'])
def groupProf(courseNum, pid):
    conn = queries.getConn('c9')
    course = queries.findCourse(conn, courseNum)
    groups = queries.groups(conn, courseNum, pid)
    numGroups = queries.numGroup(conn, courseNum, pid)
    return render_template('groupProf.html', course = course, courseNum = courseNum,
    numGroups = numGroups['numGroups'], groups = groups, logged_in = session['logged_in'])
    
    
@app.route('/uploadAjax/', methods=["POST"])
def file_upload():
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
            
        return render_template('assignment.html')
        
@app.route('/update/<pid>', methods = ['GET', 'POST'])
def deleteAssignment(pid):
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

@app.route('/newCourse', methods=['GET', 'POST'])
def newCourse():
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
    return render_template('newCourse.html', bnumber = bnumber)
        
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
