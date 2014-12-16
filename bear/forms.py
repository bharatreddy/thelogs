from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
 
class RegistrationForm(Form):
    name = TextField("Name")
    email = TextField("Email")
    password = TextField("Password")
    submit = SubmitField("Send")