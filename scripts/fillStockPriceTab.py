if __name__ == "__main__":
    import time
    import fillStockPriceTab
    stp = fillStockPriceTab.FillStockPriceTable()
    while True:
        stp.active_stock_prices()
        time.sleep(60.)

class FillStockPriceTable(object):
    """
    A class to fill in the stock prices table,
    with current price details from yahoo finance.
    """

    def __init__(self):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # get a list of all symbols in StockSymbols table
        qrySyms = ("""
            SELECT DISTINCT stocksymbol
            FROM StockSymbols
            """)
        self.cursor.execute(qrySyms)
        self.allSymList = [s[0] for s in self.cursor]
        # get a list of active stocks
        qrySyms = ("""
            SELECT DISTINCT stock_symbol
            FROM stockTransactions
            """)
        self.cursor.execute(qrySyms)
        self.actvSymList = [s[0] for s in self.cursor]

    def update_sym_list(self):
        # update/insert symbol list in the StockPrices table
        for st in self.allSymList:
            query = ("INSERT INTO StockPrices "
                   " (stock_symbol, NSE_cost_per_unit, NSE_datetime, BSE_cost_per_unit, BSE_datetime) "
                   " VALUES (%s, %s, %s, %s, %s) "
                   " ON DUPLICATE KEY UPDATE "
                   "   stock_symbol=VALUES(stock_symbol), "
                   "   NSE_cost_per_unit=VALUES(NSE_cost_per_unit), "
                   "   NSE_datetime=VALUES(NSE_datetime), "
                   "   BSE_cost_per_unit=VALUES(BSE_cost_per_unit), "
                   "   BSE_datetime=VALUES(BSE_datetime) "
                   )
            params = (
                st, 
                None, 
                None, 
                None, 
                None)
            self.cursor.execute(query, params)
            self.conn.commit()

    def fill_stock_price_tab(self):
        import stockPrice
        import datetime
        from pytz import timezone
        # the date string we get has the following format
        # 23 Dec 3:29pm
        dtFormat = "%d %b %I:%M%p"
        # loop through the symbols in the list and
        # fill current stock price into the table.
        for stsym in self.allSymList:
            nseObj = stockPrice.GetStockPrice(stsym, exchange='NSE')
            bseObj = stockPrice.GetStockPrice(stsym, exchange='BSE')
            try:
                (currNSEDate, currNSEPrice) = nseObj.get_stock_data()
                currNSEPrice = float(currNSEPrice.replace(",", ""))
                try:
                    # convert the datetime string to python datetime object
                    currNSEDate = datetime.datetime.strptime(currNSEDate, dtFormat)
                    # need to set the year as we dont get 
                    # the information from the string.
                    # get the current year
                    currYear = datetime.datetime.utcnow().year
                    currNSEDate = currNSEDate.replace(year=2014)
                except:
                    # if is fails get current time in india
                    currNSEDateUTC = datetime.datetime.now(timezone('UTC'))
                    currNSEDate = currNSEDateUTC.astimezone(timezone('Asia/Kolkata'))
            except:
                (currNSEDate, currNSEPrice) = (None,None)
            try:
                (currBSEDate, currBSEPrice) = bseObj.get_stock_data()
                currBSEPrice = float(currBSEPrice.replace(",", ""))
                try:
                    currBSEDate = datetime.datetime.strptime(currBSEDate, dtFormat)
                    # need to set the year as we dont get 
                    # the information from the string.
                    # get the current year
                    currYear = datetime.datetime.utcnow().year
                    currBSEDate = currBSEDate.replace(year=2014)
                except:
                    # if is fails get current time in india
                    currBSEDateUTC = datetime.datetime.now(timezone('UTC'))
                    currBSEDate = currBSEDateUTC.astimezone(timezone('Asia/Kolkata'))
            except:
                (currBSEDate, currBSEPrice) = (None,None)
            print stsym, currNSEDate, currNSEPrice, currBSEDate, currBSEPrice
            # fill in the price info in the tables
            # Now if we have None values in both BSE and NSE prices don't update
            if ( (currNSEPrice is None) and (currBSEPrice is None) ):
                continue
            elif ( (currNSEPrice is None) and (currBSEPrice is not None) ):
                try:
                    query = ("INSERT INTO StockPrices "
                           " (stock_symbol, BSE_cost_per_unit, BSE_datetime) "
                           " VALUES (%s, %s, %s) "
                           " ON DUPLICATE KEY UPDATE "
                           "   stock_symbol=VALUES(stock_symbol), "
                           "   BSE_cost_per_unit=VALUES(BSE_cost_per_unit), "
                           "   BSE_datetime=VALUES(BSE_datetime) "
                           )
                    params = (
                        stsym,
                        currBSEPrice, 
                        currBSEDate)
                    self.cursor.execute(query, params)
                    self.conn.commit()
                except:
                    print "-------------------------INSERT FAILED-------------------------"
            elif ( (currNSEPrice is not None) and (currBSEPrice is None) ):
                try:
                    query = ("INSERT INTO StockPrices "
                           " (stock_symbol, BSE_cost_per_unit, BSE_datetime) "
                           " VALUES (%s, %s, %s) "
                           " ON DUPLICATE KEY UPDATE "
                           "   stock_symbol=VALUES(stock_symbol), "
                           "   NSE_cost_per_unit=VALUES(NSE_cost_per_unit), "
                           "   NSE_datetime=VALUES(NSE_datetime) "
                           )
                    params = (
                        stsym,
                        currNSEPrice, 
                        currNSEDate)
                    self.cursor.execute(query, params)
                    self.conn.commit()
                except:
                    print "-------------------------INSERT FAILED-------------------------"
            else:
                try:
                    query = ("INSERT INTO StockPrices "
                           " (stock_symbol, NSE_cost_per_unit, NSE_datetime, BSE_cost_per_unit, BSE_datetime) "
                           " VALUES (%s, %s, %s, %s, %s) "
                           " ON DUPLICATE KEY UPDATE "
                           "   stock_symbol=VALUES(stock_symbol), "
                           "   NSE_cost_per_unit=VALUES(NSE_cost_per_unit), "
                           "   NSE_datetime=VALUES(NSE_datetime), "
                           "   BSE_cost_per_unit=VALUES(BSE_cost_per_unit), "
                           "   BSE_datetime=VALUES(BSE_datetime) "
                           )
                    params = (
                        stsym, 
                        currNSEPrice, 
                        currNSEDate, 
                        currBSEPrice, 
                        currBSEDate)
                    self.cursor.execute(query, params)
                    self.conn.commit()
                except:
                    print "-------------------------INSERT FAILED-------------------------"

    def active_stock_prices(self):
        import stockPrice
        import datetime
        # the date string we get has the following format
        # 23 Dec 3:29pm
        dtFormat = "%d %b %I:%M%p"
        dtFormat2 = "%I:%M%p"
        # loop through the symbols in the list and
        # fill current stock price into the table.
        for stsym in self.actvSymList:
            nseObj = stockPrice.GetStockPrice(stsym, exchange='NSE')
            bseObj = stockPrice.GetStockPrice(stsym, exchange='BSE')
            try:
                (currNSEDate, currNSEPrice) = nseObj.get_stock_data()
                currNSEPrice = float(currNSEPrice.replace(",", ""))
                try:
                    # convert the datetime string to python datetime object
                    if len(currNSEDate) < 10:
                        currNSEDate = datetime.datetime.strptime(currNSEDate, dtFormat2)
                    else:
                        currNSEDate = datetime.datetime.strptime(currNSEDate, dtFormat)
                    # need to set the year as we dont get 
                    # the information from the string.
                    # get the current year
                    currYear = datetime.datetime.utcnow().year
                    currMonth = datetime.datetime.utcnow().month
                    currDay = datetime.datetime.utcnow().day
                    currNSEDate = currNSEDate.replace(\
                        year=currYear, month=currMonth, day=currDay)
                except:
                    # if is fails get current time in india
                    currNSEDateUTC = datetime.datetime.now(timezone('UTC'))
                    currNSEDate = currNSEDateUTC.astimezone(timezone('Asia/Kolkata'))
            except:
                (currNSEDate, currNSEPrice) = (None,None)
            try:
                (currBSEDate, currBSEPrice) = bseObj.get_stock_data()
                currBSEPrice = float(currBSEPrice.replace(",", ""))
                try:
                    if len(currBSEDate) < 10:
                        currBSEDate = datetime.datetime.strptime(currBSEDate, dtFormat2)
                    else:
                        currBSEDate = datetime.datetime.strptime(currBSEDate, dtFormat)
                    # need to set the year as we dont get 
                    # the information from the string.
                    # get the current year
                    currYear = datetime.datetime.utcnow().year
                    currMonth = datetime.datetime.utcnow().month
                    currDay = datetime.datetime.utcnow().day
                    currBSEDate = currBSEDate.replace(\
                        year=currYear, month=currMonth, day=currDay)
                except:
                    # if is fails get current time in india
                    currBSEDateUTC = datetime.datetime.now(timezone('UTC'))
                    currBSEDate = currBSEDateUTC.astimezone(timezone('Asia/Kolkata'))
            except:
                (currBSEDate, currBSEPrice) = (None,None)
            print stsym, currNSEDate, currNSEPrice, currBSEDate, currBSEPrice
            # fill in the price info in the tables
            # Now if we have None values in both BSE and NSE prices don't update
            if ( (currNSEPrice is None) and (currBSEPrice is None) ):
                continue
            try:
                query = ("INSERT INTO StockPrices "
                       " (stock_symbol, NSE_cost_per_unit, NSE_datetime, BSE_cost_per_unit, BSE_datetime) "
                       " VALUES (%s, %s, %s, %s, %s) "
                       " ON DUPLICATE KEY UPDATE "
                       "   stock_symbol=VALUES(stock_symbol), "
                       "   NSE_cost_per_unit=VALUES(NSE_cost_per_unit), "
                       "   NSE_datetime=VALUES(NSE_datetime), "
                       "   BSE_cost_per_unit=VALUES(BSE_cost_per_unit), "
                       "   BSE_datetime=VALUES(BSE_datetime) "
                       )
                params = (
                    stsym, 
                    currNSEPrice, 
                    currNSEDate, 
                    currBSEPrice, 
                    currBSEDate)
                self.cursor.execute(query, params)
                self.conn.commit()
            except:
                print "-------------------------INSERT FAILED-------------------------"