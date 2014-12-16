from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = '@dec152014#'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True

import bear.routes