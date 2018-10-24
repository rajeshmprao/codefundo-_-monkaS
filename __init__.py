from flask import Flask, render_template, flash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import sys
import os
class RegistrationForm(Form):
    missing_name = TextField('Missing Person Name', [validators.Length(min=4, max=20)])
    latitude = TextField('Latitude', [validators.Required()])
    longitude = TextField('Longitude', [validators.Required()])
    name = TextField('Your Name', [validators.Length(min=4, max=20)])
    mobile = TextField('Your Mobile Number', [validators.Length(min=6, max=12)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    
'''
class RegistrationForm(Form):
    missing_name = TextField('Missing Person Name', [validators.Length(min=4, max=20)])
    latitude = TextField('Latitude', [validators.Required()])
    longitude = TextField('Longitude', [validators.Required()])
    name = TextField('Your Name', [validators.Length(min=4, max=20)])
    mobile = TextField('Your Mobile Number', [validators.Length(min=6, max=12)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
'''    

app = Flask(__name__)
app.secret_key = os.environ['secret']

@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/helpme/')
def helpme():
    return render_template('helpme.html')

@app.route('/report/', methods = ["GET", "POST"])

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
def locate():
    return render_template('locate.html')

@app.route('/map/')
def map():
    return render_template('map.html')

@app.route('/login/')
def login():
    flash('Login ples')
    return render_template('login.html')

@app.route('/register/')
def register():
    flash('register ples')
    return render_template('register.html')

if __name__ == "__main__":
    app.run()
