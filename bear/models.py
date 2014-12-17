from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
# set up the DB
dbAlc = SQLAlchemy()
# create a user class
class User(dbAlc.Model):
    __tablename__ = 'Users'
    userid = dbAlc.Column(dbAlc.Integer, primary_key = True)
    name = dbAlc.Column(dbAlc.String(100))
    email = dbAlc.Column(dbAlc.String(120), unique=True)
    pwdhash = dbAlc.Column(dbAlc.String(54))
    def __init__(self, name, email, password):
        self.name = name.title()
        self.email = email.lower()
        self.set_password(password)
    # generate a password hash 
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
    # verify password in subsequent logins
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)