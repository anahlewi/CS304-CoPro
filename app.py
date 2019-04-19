from flask import (Flask, url_for, render_template, request, redirect, flash, session)
import random,math
app = Flask(__name__)

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
                           
# conn = movieDatabase.getConn('c9')
#url build so that the user comes first then build off ie mhardy2/course/assignments

@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/courses')
def courses():
    return render_template('courses.html')
    
@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/profile')
def profile():
    user = None
    return render_template('profile.html', user=user)
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)