from wtforms import Form, BooleanField, TextField, PasswordField, SelectField, validators

class register_form(Form):

    email = TextField('Email Address', [validators.Length(min=6, max=50), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Error. Passwords must match")])
    confirm = PasswordField('Confirm Password')
    username = TextField('username', [validators.Length(min=6, max=50), validators.Required()])
    accept_tos = BooleanField('I accept the Terms of Service', [validators.Required()])
    name = TextField('Your Name', [validators.Length(min=4, max=20), validators.Required()])
    mobile = TextField('Your Mobile Number', [validators.Length(min=6, max=12), validators.Required()])
    myChoices = [('relief', 'Relief Worker'), ('report', 'Reporter')]
    role = SelectField('I am A: ', choices = myChoices, validators = [validators.Required()])
