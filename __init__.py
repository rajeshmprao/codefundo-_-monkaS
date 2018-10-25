from flask import Flask, render_template, flash, url_for, redirect, request, session
import sys
from forms import register_form
from passlib.hash import sha256_crypt
from functools import wraps
import pymysql
from pymysql import escape_string as thwart
from flaskapp_db.connections import cursor_conn
import gc 

import os


app = Flask(__name__)
# app.secret_key = os.environ['secret']

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session)
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


def relief_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == 'relief' :
            return f(*args, **kwargs)
        elif 'logged_in' in session and session['logged_in'] == 'report' :
            flash("Logout and login as relief worker")
            return redirect(url_for('homepage'))
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
        
    return wrap

def report_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == 'report' :
            return f(*args, **kwargs)
        elif 'logged_in' in session and session['logged_in'] == 'relief' :
            flash("Logout and login as reporter")
            return redirect(url_for('homepage'))
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap
    


@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/helpme/')
def helpme():
    return render_template('helpme.html')

@app.route('/report/', methods = ["GET", "POST"])
@report_login_required
def report():
    # try:
    #     form = RegistrationForm(request.form)

    #     if request.method == "POST" and form.validate():
    #         missing_name = form.missing_name.data 
    #     latitude = form.latitude.data
    #     longitude = form.longitude.data
    #     name = form.name.data
    #     mobile = form.mobile.data
    #     email = form.email.data
    #     c, conn = connection()

    #     x = c.execute("SELECT * FROM users WHERE username = (%s)",
    #                     (thwart(username)))

    #     if int(x) > 0:
    #         flash("That username is already taken, please choose another")
    #         return render_template('register.html', form=form)

    #     else:
    #         c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
    #                     (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
            
    #         conn.commit()
    #         flash("Thanks for registering!")
    #         c.close()
    #         conn.close()
    #         gc.collect()

    #         session['logged_in'] = True
    #         session['username'] = username

    #         return redirect(url_for('dashboard'))

    # return render_template("register.html", form=form)

    # except Exception as e:
    #     return(str(e))
    return render_template('report.html')

@app.route('/locate/')
@relief_login_required
def locate():
    return render_template('locate.html')

@app.route('/map/')
# @relief_login_required
def map():
    return render_template('map.html')

@app.route('/geolocation/')
def geolocation():
    return render_template('geolocation.html')

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))

@app.route('/login/', methods = ["GET", "POST"])
def login():
    error = ''
    try:
        c, conn = cursor_conn()
        role_dict = {"Login as Reporter":"report", "Login as Relief Worker":"relief"}
        if request.method == "POST":
            c.execute("USE FLASKAPP;")
            data = c.execute("SELECT password FROM users WHERE username = (%s) and role = (%s) ",
                                (thwart(request.form['username']), thwart(role_dict[request.form['action']])))
            data = c.fetchone()['password']
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = role_dict[request.form['action']]
                session['username'] = request.form['username']
                print(session)

                flash("Logged in successfully")

                if role_dict[request.form['action']] == 'relief':
                    return redirect(url_for('locate'))
                elif role_dict[request.form['action']] == 'report':
                    return redirect(url_for('report'))
            
            else:
                error = "Invalid credentials, try again."            
            gc.collect()
            flash(error)    
            return render_template("login.html")

    except Exception as e:
        raise
        error = "Account does not exist. Click signup to create one."
        flash(error)
        return render_template("login.html")
        
    return render_template('login.html' )


@app.route('/register/', methods = ["GET", "POST"])
def register():
    form = register_form(request.form)
    if request.method == "POST":
        if form.validate():
            mobile = form.mobile.data
            email = form.email.data
            name = form.name.data
            username = form.username.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            role = form.role.data

            c, conn = cursor_conn()
            x = c.execute("SELECT * FROM FLASKAPP.users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
                try:
                    c.execute("INSERT INTO FLASKAPP.users (email, password, name, mobile, role, username) VALUES (%s, %s, %s, %s, %s, %s)",
                            (thwart(email), thwart(password), thwart(name), thwart(mobile), thwart(role), thwart(username)))
                    
                    flash("Thanks for registering!")
                except:
                    flash("That Mobile number is already taken, please choose another")
                    return render_template('register.html', form=form)
               
                c.close()
                conn.close()
                gc.collect()
            
            session['logged_in'] = role
            session['username'] = username

            if role == 'relief':
                return redirect(url_for('locate'))
            elif role == 'report':
                return redirect(url_for('report'))
        else:
            flash("Error in form. Please Fill Again")
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
