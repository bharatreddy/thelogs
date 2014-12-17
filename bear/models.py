from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
# set up the DB
dbAlc = SQLAlchemy()
# create a user class
class User(db.Model):
    __tablename__ = 'Users'
    userid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))
    def __init__(self, name, lastname, email, password):
        self.name = name.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
    # generate a password hash 
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
    # verify password
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)