from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, \
validators, ValidationError, DateTimeField, IntegerField, FloatField, SelectField
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
    password = PasswordField("Password", [validators.Required("password")])
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

class InputTransForm(Form):
    # get the list of stock symbols
    dbRaw = \
        MySQLdb.connect( user='root', host='localhost', port=3306, db='Logbook' )
    querySrchStr = "SELECT stocksymbol, stockname FROM StockSymbols"
    dbRaw.query( querySrchStr )
    query_results = dbRaw.store_result().fetch_row( maxrows=0 )
    stckList = [ (res[0], res[0]) for res in query_results ]
    # form to record new transactions
    date = DateTimeField("Transaction Date", format='%d/%m/%Y %H:%M')
    transType = SelectField("Transaction Type",\
     choices = [("1","Buy"), ("2","Sell")])
    quantity = IntegerField("Num of Shares",  \
         [validators.NumberRange(min=0, max=10000000)])
    unitPrice = FloatField('unit price', [validators.Required("unit price")])
    stockSymbol = SelectField("Stock Symbols",\
     choices = stckList)
    #TextField("Stock Symbol",  [validators.Required("Stock Symbol")],id='stSymAuto')
    simulated = SelectField("Simulated",\
     choices = [("No","No"), ("Yes","Yes")])
    submit = SubmitField("Submit")
   
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    # validate the form    
    def validate(self):
        if not Form.validate(self):
            return False