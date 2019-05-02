import json
import queries 
from flask import (Flask, url_for, redirect, session, render_template, request, flash)
import random, math
from flask_login import (UserMixin, login_required, login_user, logout_user, current_user)
from flask_googlelogin import GoogleLogin



app = Flask(__name__)
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
    return render_template('profile.html', user=userInfo)
    
    
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
    if courseNum:
        conn = queries.getConn('c9')
        course = queries.findCourse(conn, courseNum)
        roster = queries.roster(conn, courseNum)
        print(course['courseName'])
        return render_template('roster.html', course = course, roster = roster)
    else:
        conn = queries.getConn('c9')
        courses = queries.courses(conn)
        return render_template('courses.html', courses = courses)

    
@app.route('/update', methods =['POST'])
def update():
    if session.get('logged_in'):
        conn = queries.getConn('c9')
        name = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bnumber = request.form.get('bnumber')
        residence = request.form.get('residence')
        avail= request.form.get('avail')
    
        try:
            updated = queries.update(conn, name, email, phone, residence, avail)
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
@app.route('/assignments', methods = ['GET'])
# @login_required
def assignments(): #I assume we're going to be grabbing assignments for a particular course
    conn = queries.getConn('c9')
    courseNum = '13587'
    psets = queries.getAssignments(conn, courseNum)
    return render_template('assignments.html', psets = psets)

@app.route('/search', methods = ['POST'])
def search():
    title = request.form.get('searchterm')
    
    return redirect
    
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
