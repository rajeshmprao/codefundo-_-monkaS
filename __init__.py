from flask import Flask, render_template, flash, url_for, redirect, request, session
import sys
from forms import register_form
from passlib.hash import sha256_crypt
from functools import wraps
import pymysql
from pymysql import escape_string as thwart
from flaskapp_db.connections import cursor_conn
import gc 
from OpenSSL import SSL

import os


#context = SSL.Context(SSL.SSLv23_METHOD)
# context = ('host.cert','host.key')
#context.use_privatekey_file('host.key')
#context.use_certificate_file('host.cert')
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
            flash("You need to login first as relief worker")
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
            flash("You need to login as reporter")
            return redirect(url_for('login'))
    return wrap

def logout_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session)
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash("You need to logout first")
            return redirect(url_for('homepage'))
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
    try:
        if request.method == "POST":
            name = request.form["name"]
            latitude = request.form["latitude"]
            longitude = request.form["longitude"]
            mobile = request.form["mobile"]
            if name == "" or latitude == "" or longitude == "" or mobile == "":
                flash("Please fill corect data")
                return render_template('report.html')
            c, conn = cursor_conn()

            x = c.execute("SELECT mobile FROM FLASKAPP.users WHERE username = (%s)",
                            (thwart(session['username'])))
            usermobile = c.fetchone()['mobile']
            c.execute("INSERT INTO FLASKAPP.victims (name, reporterMobile, mobile, latitude, longitude, status) VALUES (%s, %s, %s, %s, %s, %s)",
                        (thwart(name), thwart(usermobile), thwart(mobile), thwart(latitude), thwart(longitude), thwart("not_rescued")))

            conn.commit()
            flash("Person Added. Relief workers will find for your loved one!")
            c.close()
            conn.close()
            gc.collect()

            return redirect(url_for('report'))
        return render_template("report.html")

    except pymysql.IntegrityError as e:
        flash("Person has already been reported")
        return render_template('report.html')
    except Exception as e:
        flash("Please fill corect data")
        return render_template('report.html')
        

@app.route('/check/')
@report_login_required
def check():
    try:
        c, conn = cursor_conn()

        x = c.execute("SELECT mobile FROM FLASKAPP.users WHERE username = (%s)",
                        (thwart(session['username'])))
        usermobile = c.fetchone()['mobile']
        print(usermobile)
        c.execute("SELECT name, mobile, status from FLASKAPP.victims WHERE reporterMobile =  (%s)",
                    (thwart(usermobile)))

        result = c.fetchall()
        if len(result) == 0:
            flash("No victims reported")
            return render_template('report.html')
        c.close()
        conn.close()
        gc.collect()
        return render_template("check.html", result = result)

    except Exception as e:
        raise
        flash("No victims reported")
        return render_template('report.html')


@app.route('/locate/')
@relief_login_required
def locate():
    c, conn = cursor_conn()
    x = c.execute("SELECT name, latitude, longitude FROM FLASKAPP.victims WHERE status = 'not_rescued'")
    variable = c.fetchall()
    return render_template('locate.html', variable = variable)

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

@app.route('/update/', methods = ["GET", "POST"])
@relief_login_required
def update():
    try:
        if request.method == "POST":
            mobile = request.form["mobile"]
            if mobile == "":
                flash("Please fill corect data")
                return render_template('update.html')
            c, conn = cursor_conn()

            x = c.execute("SELECT * FROM FLASKAPP.victims WHERE mobile = (%s)",
                            (thwart(mobile)))
            if int(x) <= 0:
                flash("This mobile number has not been reported")
                return render_template("update.html")

            x = c.execute("UPDATE FLASKAPP.victims SET status = %s WHERE mobile= (%s)",
                        (thwart(request.form['action']), thwart(mobile)))

            conn.commit()
            flash("Person Status updated to {}".format(request.form['action']))
            c.close()
            conn.close()
            gc.collect()

        return render_template("update.html")

    except Exception as e:
        raise
        flash("Please fill corect data")
        return render_template('report.html')


@app.route('/login/', methods = ["GET", "POST"])
@logout_required
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
                return redirect(url_for('homepage'))            
            else:
                error = "Invalid credentials, try again."            
            gc.collect()
            flash(error)    
            return render_template("login.html")

    except Exception as e:
        error = "Account does not exist. Click signup to create one."
        flash(error)
        return render_template("login.html")
        
    return render_template('login.html' )


@app.route('/register/', methods = ["GET", "POST"])
@logout_required
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
            return render_template('main.html')
            
        else:
            flash("Error in form. Please Fill Again")
    return render_template('register.html', form=form)

if __name__ == "__main__":
    # app.run(ssl_context=context)
    app.run()
