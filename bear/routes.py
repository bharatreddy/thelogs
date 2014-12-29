from bear import app
from flask import Flask, Response,render_template, \
request, jsonify, flash, session, redirect, url_for
from forms import RegistrationForm, SigninForm, InputTransForm
from flask.ext.mail import Message, Mail
import MySQLdb
import json
from models import dbAlc, User
import mysql.connector

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
    queryUserChk = " SELECT userid, name FROM Users WHERE email = " \
    + "'" + session['email'] + "'"
    dbRaw.query( queryUserChk )
    userDetails = dbRaw.store_result().fetch_row( maxrows=0 )
    # check if we have the email in our database of users.
    if userDetails is None:
        return redirect(url_for('signin'))
    else:
        userId = userDetails[0][0]
        userName = userDetails[0][1]
        # get number of active stocks (sell-buy>0), 
        # prices of shares for the user
        actvStcks = getActiveStocks(userId)
        transStcks = getTransactions(userId)
        # to use it in jinja templates, we need to convert the DF
        # into a list of dicts
        actvStcks = actvStcks.T.to_dict().values()
        transStcks = transStcks.T.to_dict().values()
        return render_template('profile_layout.html', \
            profileName=userName, \
            activeStocks=actvStcks, transctnStcks=transStcks)

def getTransactions(userId):
    # get acvtive shares of the user along with the current price
    import pandas
    import numpy
    qryTransactions = "select st.stock_symbol, st.stock_exchange, st. date, st.quantity, " +\
                    "st.cost_per_unit,st.quantity*st.cost_per_unit as total_cost, " +\
                    "tt.transaction_type FROM stockTransactions as st "+\
                    " INNER JOIN " +\
                    "TransactionTypes as tt ON "+\
                    "st.transaction_type_id=tt.transaction_type_id" + \
                    " WHERE st.userid = "+ str(userId) + " limit 10;"
    # set up connections to the DB
    conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
    transactionsDF = pandas.read_sql( qryTransactions, conn )
    # limit the total cost to 2 decimal places
    transactionsDF['total_cost'] = \
    transactionsDF['total_cost'].apply(lambda x: round(x, 2))
    return transactionsDF

def getActiveStocks(userId):
    # get acvtive shares of the user along with the current price
    import pandas
    import numpy
    qryNumStocks = "SELECT stock_symbol,stock_exchange,"+\
        "sum(quantity*(case when transaction_type_id=1 then 1 else -1 end)) as active_num"+\
        " FROM stockTransactions WHERE "+ "userid = "+ str(userId)+\
        " GROUP BY stock_symbol, stock_exchange;"
    # set up connections to the DB
    conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
    numStocksDF = pandas.read_sql( qryNumStocks, conn )
    # we only need stocks which currently have shares
    numStocksDF = numStocksDF[numStocksDF['active_num'] > 0].reset_index(drop=True)
    # get a list of the active stocks to retreive the current price
    actvStockList = numStocksDF['stock_symbol'].tolist()
    stckList = ""
    for nst, stsym in enumerate(actvStockList):
        stckList += "'"+stsym+"'"
        if nst < len(actvStockList)-1:
            stckList += ", "
    qryCurrPrice = "SELECT * FROM StockPrices WHERE stock_symbol IN (" \
        + stckList + ")"
    actvPrcDF = pandas.read_sql( qryCurrPrice, conn )
    # merge the DFs
    actvStcksDF = pandas.merge( numStocksDF, actvPrcDF, on='stock_symbol' )
    # Before we do further calculations, replace all None types to zero and 
    # then get them back to None types. We get None's when the stock price update
    # fails.
    actvStcksDF = actvStcksDF.fillna(0)
    # Now calculate the revenue and other values based on the stock exchange
    actvStcksDF['revenue'] = actvStcksDF.apply( \
        lambda row: row['active_num']*row['NSE_cost_per_unit'] \
        if row['stock_exchange'] == 'NSE' \
        else row['active_num']*row['BSE_cost_per_unit'], axis=1)
    actvStcksDF['current_price'] = actvStcksDF.apply( \
        lambda row: row['NSE_cost_per_unit'] \
        if row['stock_exchange'] == 'NSE' \
        else row['BSE_cost_per_unit'], axis=1)
    actvStcksDF['price_updated'] = actvStcksDF.apply( \
        lambda row: row['NSE_datetime'] \
        if row['stock_exchange'] == 'NSE' \
        else row['BSE_datetime'], axis=1)
    # if there are any zeros, print an error message
    actvStcksDF[actvStcksDF['revenue'] == 0] = "System not updating"
    return actvStcksDF

@app.route("/newtrans", methods=['GET', 'POST'])
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
    queryUserChk = " SELECT name, userid FROM Users WHERE email = " \
    + "'" + session['email'] + "'"
    dbRaw.query( queryUserChk )
    userDetails = dbRaw.store_result().fetch_row( maxrows=0 )
    userName = userDetails[0][0]
    currUserId = userDetails[0][1]
    if userDetails is None:
        return redirect(url_for('signin'))
    else:
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('transactions.html', \
                    form=form, profileName=userName, transMessage="" )
            else:
                # Nothing wrong with the form.
                # Enter into the database
                # set up connections to the DB
                conn = mysql.connector.Connect(host='localhost',user='root',\
                                        password='',database='Logbook')
                cursor = conn.cursor()
                # build necessary parameters for the query

                query = ("INSERT INTO StockTransactions "
                       " (userid, stock_symbol, date, transaction_type_id, quantity, cost_per_unit, stock_exchange, simulated) "
                       " VALUES (%s, %s,%s, %s,%s, %s, %s, %s) "
                       " ON DUPLICATE KEY UPDATE "
                       "   userid=VALUES(userid), "
                       "   stock_symbol=VALUES(stock_symbol), "
                       "   date=VALUES(date), "
                       "   transaction_type_id=VALUES(transaction_type_id), "
                       "   quantity=VALUES(quantity), "
                       "   cost_per_unit=VALUES(cost_per_unit), "
                       "   stock_exchange=VALUES(stock_exchange), "
                       "   simulated=VALUES(simulated) ")
                params = (
                    currUserId, 
                    form.stockSymbol.data,
                    form.date.data,
                    int(form.transType.data),
                    form.quantity.data,
                    form.unitPrice.data,
                    form.exchange.data,
                    form.simulated.data
                    )
                cursor.execute(query, params)
                conn.commit()
                # If all is good get the profile page of the user
                return redirect(url_for('profile'))
        elif request.method == 'GET':
            return render_template('transactions.html', \
                form=form, profileName=userName)

@app.route("/summary")
def summary():
    # fucntion to access the profile page of the user
    if 'email' not in session:
        return redirect(url_for('signin'))
    # Check if the user is in our db
    user = User.query.filter_by(email = session['email']).first()
    dbRaw = \
    MySQLdb.connect( user='root', host='localhost', port=3306, db='Logbook' )
    # check if the email-id is already taken
    queryUserChk = " SELECT userid, name FROM Users WHERE email = " \
    + "'" + session['email'] + "'"
    dbRaw.query( queryUserChk )
    userDetails = dbRaw.store_result().fetch_row( maxrows=0 )
    # check if we have the email in our database of users.
    if userDetails is None:
        return redirect(url_for('signin'))
    else:
        userId = userDetails[0][0]
        userName = userDetails[0][1]
        # get number of active stocks (sell-buy>0), 
        # prices of shares for the user
        actvStcks = getActiveStocks(userId)
        # to use it in jinja templates, we need to convert the DF
        # into a list of dicts
        actvStcks = actvStcks.T.to_dict().values()
        smryTransactions = getProfitLoss(userId)
        smryTransactions = smryTransactions.T.to_dict().values()
        return render_template('summary.html', \
            summaryTrans=smryTransactions)

def getProfitLoss(userId):
    # get acvtive shares of the user along with the current price
    import pandas
    import numpy
    # set up connections to the DB
    conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
    qrySellStocks = "SELECT stock_symbol,stock_exchange,"+\
        "SUM(quantity) as quantity_sell, cost_per_unit as unit_price_sell, "+\
        "SUM(quantity*cost_per_unit) as total_cost_sell"+\
        " FROM stockTransactions INNER JOIN transactionTypes ON "+\
        " transactionTypes.transaction_type_id"+\
        "=stockTransactions.transaction_type_id " +\
        "WHERE ("+ "userid = "+ str(userId)+\
        " and transaction_type='SELL')"+\
        "GROUP BY stock_symbol,stock_exchange;"
    sellStocksDF = pandas.read_sql( qrySellStocks, conn )
    qryBuyStocks = "SELECT stock_symbol,stock_exchange,"+\
        "SUM(quantity) as quantity_buy, cost_per_unit as unit_price_buy, "+\
        "SUM(quantity*cost_per_unit) as total_cost_buy"+\
        " FROM stockTransactions INNER JOIN transactionTypes ON "+\
        " transactionTypes.transaction_type_id"+\
        "=stockTransactions.transaction_type_id " +\
        "WHERE ("+ "userid = "+ str(userId)+\
        " and transaction_type='BUY')"+\
        "GROUP BY stock_symbol,stock_exchange;"
    buyStocksDF = pandas.read_sql( qryBuyStocks, conn )
    # we have a buy and sell dataset, now merge the two DFs
    # and calculate profit/loss
    prftStcksDF = pandas.merge( buyStocksDF, sellStocksDF,\
     on=['stock_symbol','stock_exchange'] )
    # now profit is calculated based on number of shares sold.
    # Now calculating the profits is complicated, we could have 
    # multiple transactions of buy and sell. so we'll calcualte the 
    # buy price as total_buy_price multiplied by fraction of shares sold.
    # Ofcourse, cost of shares sold is simpler.
    prftStcksDF['profit'] = (prftStcksDF['total_cost_sell']*1.) \
    - (prftStcksDF['quantity_sell']*1./prftStcksDF['quantity_buy'])*\
    prftStcksDF['total_cost_buy'] 
    # limit to 2 decimal places.
    prftStcksDF['profit'] = \
    prftStcksDF['profit'].apply(lambda x: round(x, 2))
    return prftStcksDF

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