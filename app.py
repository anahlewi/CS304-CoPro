from flask import (Flask, url_for, render_template, request, redirect, flash, session)
import random,math
app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
                           
# conn = movieDatabase.getConn('c9')

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/dashboard/<user>")
def dashboard(user):
    return render_template("dashboard.html")
    
@app.route("/match/<user>")
def match(user):
    return render_template("match.html")

@app.route("/profile/<user>")
def profile(user):
    return render_template("profile.html")
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)