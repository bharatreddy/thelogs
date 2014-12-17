from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators, ValidationError
from models import dbAlc, User
import MySQLdb
 
class RegistrationForm(Form):
    name = TextField("Name",  [validators.Required("Name")])
    email = TextField("Email",  [validators.Required("Email")])
    password = PasswordField("Password", [validators.Required("password.")])
    confirmpassword = PasswordField("Confirm Password",\
     [validators.Required("Confirm Password")])
    submit = SubmitField("Create Account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    # validate the form
    def validate(self):
        if not Form.validate(self):
            return False
        # check if the confirm password and password are the same
        if not (self.password.data == self.confirmpassword.data):
            self.password.errors.append("Password doesn't match with confirm password")
            return False
        dbRaw = \
        MySQLdb.connect( user='root', host='localhost', port=3306, db='Logbook' )
        # check if the email-id is already taken
        queryEmailChk = " SELECT email FROM Users WHERE email = " \
        + "'" + self.email.data.lower() + "'"
        dbRaw.query( queryEmailChk )
        chkEmail = dbRaw.store_result().fetch_row( maxrows=0 )
        if chkEmail :
            self.email.errors.append("The email is already taken")
            return False
        return True

class SigninForm(Form):
    email = TextField("Email",  [validators.Required("Email")])
    password = PasswordField("Password", [validators.Required("password.")])
    submit = SubmitField("Sign In")
   
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    # validate the form
    def validate(self):
        if not Form.validate(self):
            return False
     
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid email or password")
            return False
