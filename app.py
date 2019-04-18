import json

from flask import Flask, url_for, redirect, session
from flask_login import (UserMixin, login_required, login_user, logout_user, current_user)
from flask_googlelogin import GoogleLogin


users = {}

app = Flask(__name__)
app.config.update(
    SECRET_KEY='AIzaSyBbtqYZB9aGi4sPmzbKKJvpV2EpcwDY47g',
    GOOGLE_LOGIN_CLIENT_ID='137996221652-06lt05ueh81jt9rtse06idsdgggmoda5.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='lWDlIeZukzElBCdrnhidGoNR',
    GOOGLE_LOGIN_REDIRECT_URI='http://mysql-workshop-alewi.c9users.io:8081/oauth2callback',
    GOOGLE_LOGIN_SCOPES='https://www.googleapis.com/auth/userinfo.email')

googlelogin = GoogleLogin(app)

class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')
        self.email = userinfo.get('email')

@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    return redirect(params.get('next', url_for('home')))

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
    return 'Hello world'

@app.route('/home')
@login_required
def home():
    return """
        <p>Hello, %s</p>
        <p><img src="%s" width="100" height="100"></p>
        <p>Token: %r</p>
        <p>Extra: %r</p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, current_user.picture, session.get('token'),
               session.get('extra'))


@app.route('/api/addexpense')
@login_required
def api_addexpense():
    req = request.get_json()
    return req





# from flask import (Flask, url_for, render_template, request, redirect, flash, session)
# from flask_oauth import OAuth
# import random,math
# # conn = queries.getConn('c9')


 
# # You must configure these 3 values from Google APIs console
# # https://code.google.com/apis/console
# GOOGLE_CLIENT_ID = '137996221652-06lt05ueh81jt9rtse06idsdgggmoda5.apps.googleusercontent.com'
# GOOGLE_CLIENT_SECRET = 'lWDlIeZukzElBCdrnhidGoNR'
# REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
 
# SECRET_KEY = 'AIzaSyBbtqYZB9aGi4sPmzbKKJvpV2EpcwDY47g'
 
# app = Flask(__name__)
# app.secret_key = SECRET_KEY
# oauth = OAuth()
 
# google = oauth.remote_app('google',
#                           base_url='https://www.google.com/accounts/',
#                           authorize_url='https://accounts.google.com/o/oauth2/auth',
#                           request_token_url=None,
#                           request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
#                                                 'response_type': 'code'},
#                           access_token_url='https://accounts.google.com/o/oauth2/token',
#                           access_token_method='POST',
#                           access_token_params={'grant_type': 'authorization_code'},
#                           consumer_key=GOOGLE_CLIENT_ID,
#                           consumer_secret=GOOGLE_CLIENT_SECRET)
 
# @app.route('/')
# def index():
#     access_token = session.get('access_token')
#     if access_token is None:
#         return redirect(url_for('login'))
 
#     access_token = access_token[0]
#     from urllib2 import Request, urlopen, URLError
 
#     headers = {'Authorization': 'OAuth '+access_token}
#     req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
#                   None, headers)
#     email = req.method.get('email')
#     print email
#     try:
#         res = urlopen(req)
#     except URLError, e:
#         if e.code == 401:
#             # Unauthorized - bad token
#             session.pop('access_token', None)
#             return redirect(url_for('login'))
#         return res.read()
#     return res.read()
 
 
# @app.route('/login')
# def login():
#     callback=url_for('authorized', _external=True)
#     return google.authorize(callback=callback)
 
 
 
# @app.route(REDIRECT_URI)
# @google.authorized_handler
# def authorized(resp):
#     access_token = resp['access_token']
#     session['access_token'] = access_token, ''
#     return redirect(url_for('index'))
 
 
# @google.tokengetter
# def get_access_token():
#     return session.get('access_token')

    
# @app.route("/dashboard/<user>")
# def dashboard(user):
#     session.get
#     dashboardDict = queries.dashboard(conn, )
#     return render_template("dashboard.html")
    
# @app.route("/match/<user>")
# def match(user):
#     return render_template("match.html")

# @app.route("/profile/<user>")
# def profile(user):
    
#     return render_template("profile.html")

# def get_user_info():
#     credentials = build_credentials()

#     oauth = googleapiclient.discovery.build(
#                         'oauth2', 'v2',
#                         credentials=credentials)

#     return oauth.userinfo().get().execute()   
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)