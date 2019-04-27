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
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    conn = queries.getConn('c9')
    print(user.name)
    search = queries.profile(conn, user.name)
    if search:
        return redirect(params.get('next',url_for('profile')))
        
    else:
        return redirect(params.get('next', url_for('newUser')))
        

#allows user to logout for testing purpose --> more sophisticated login will be created    
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return """
        <p>Logged out</p>
        <p><a href="/">Return to /</a></p>
        """

@app.route('/')
def index():
    return render_template('base.html')

#profile page can only be accessed once you have logged in 
@app.route('/profile')
@login_required
def profile():
    conn = queries.getConn('c9')
    userInfo = queries.profile(conn, current_user.email)
    print(current_user.name)
    return render_template('profile.html', user=userInfo)
    
#will be redirected to this url when your name is not in database
@app.route('/newUser', methods = ['GET','POST'])
@login_required
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
@login_required
def courses(courseNum):
    conn = queries.getConn('c9')

    courses = queries.courses(conn, courseNum)
    return render_template('courses.html', courses = courses)
    
@app.route('/courses')
@login_required
def coursesAll():
    conn = queries.getConn('c9')
    return render_template('courses.html')
    
@app.route('/update', methods =['POST'])
@login_required
def update():
    conn = queries.getConn('c9')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    residence = request.form.get('residence')
    avail= request.form.get('avail')
    
    try:
        updated = queries.update(conn, name, email, phone, residence, avail)
    except:
        flash('Unable to Update info')
    return redirect(url_for('profile'))
    
@app.route('/home')
@login_required
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

    

    
@app.route('/assignments')
@login_required
def assignments():
    return render_template('assignments.html')


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)
