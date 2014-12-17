from bear import app
from flask import Flask, render_template, request, jsonify, flash
from forms import RegistrationForm
from flask.ext.mail import Message, Mail
import MySQLdb
import json
from models import dbAlc

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/<pagename>")
def regularpage( pagename=None ):
    """
    if route not found
    """
    return "No such page as " + pagename + " please go back!!! "

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = RegistrationForm()
    # if a GET request is sent to the server, 
    # the web page containing the form should be retrieved 
    # and loaded in browser. If the server receives a POST request,
    # a function should capture the form field data and check if it's valid.
    if request.method == 'POST':
      return 'Form posted.'
    return render_template('contact.html', form=form)

# if __name__ == "__main__":
#     app.debug=True
#     app.run()