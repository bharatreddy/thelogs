from bear import app
from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from forms import RegistrationForm, SigninForm, InputTransForm
from flask.ext.mail import Message, Mail
import MySQLdb
import json
from models import dbAlc, User

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = RegistrationForm()
    # if a GET request is sent to the server, 
    # the web page containing the form should be retrieved
    # and loaded in browser. If the server receives a POST request,
    # a function should capture the form field data and check if it's valid.
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('contact.html', form=form)
        else:
            # Nothing wrong with the form.
            # Create a new user object
            newUser = User(form.name.data, form.email.data, form.password.data)
            # Add the user to the DB
            dbAlc.session.add(newUser)
            dbAlc.session.commit()
            session['email'] = newUser.email
            # If all is good get the profile page of the user
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))             
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route("/profile")
def profile():
    # fucntion to access the profile page of the user
    if 'email' not in session:
        return redirect(url_for('signin'))
    # Check if the user is in our db
    user = User.query.filter_by(email = session['email']).first()
    dbRaw = \
    MySQLdb.connect( user='root', host='localhost', port=3306, db='Logbook' )
    # check if the email-id is already taken
    queryUserChk = " SELECT name FROM Users WHERE email = " \
    + "'" + session['email'] + "'"
    dbRaw.query( queryUserChk )
    userDetails = dbRaw.store_result().fetch_row( maxrows=0 )
    userName = userDetails[0][0]
    if userDetails is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile_layout.html', profileName=userName)

@app.route("/newtrans")
def newtrans():
    form = InputTransForm()
    # fucntion to access the profile page of the user
    if 'email' not in session:
        return redirect(url_for('signin'))
    # Check if the user is in our db
    user = User.query.filter_by(email = session['email']).first()
    dbRaw = \
    MySQLdb.connect( user='root', host='localhost', port=3306, db='Logbook' )
    # check if the email-id is already taken
    queryUserChk = " SELECT name FROM Users WHERE email = " \
    + "'" + session['email'] + "'"
    dbRaw.query( queryUserChk )
    userDetails = dbRaw.store_result().fetch_row( maxrows=0 )
    userName = userDetails[0][0]
    if userDetails is None:
        return redirect(url_for('signin'))
    else:
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('transactions.html', \
                    form=form, profileName=userName)
            else:
                session['email'] = form.email.data
                return redirect(url_for('profile'))             
        elif request.method == 'GET':
            return render_template('transactions.html', \
                form=form, profileName=userName)

@app.route("/signout")
def signout(): 
    if 'email' not in session:
        return redirect(url_for('signin'))
    session.pop('email', None)
    return redirect(url_for("home"))

@app.route("/<pagename>")
def regularpage( pagename=None ):
    """
    if route not found
    """
    return "No such page as " + pagename + " please go back!!! "

# if __name__ == "__main__":
#     app.debug=True
#     app.run()