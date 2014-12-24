if __name__ == "__main__":
    import fillStockPriceTab
    stp = fillStockPriceTab.FillStockPriceTable()
    stp.fill_stock_price_tab()

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
        self.symList = [s[0] for s in self.cursor]

    def fill_stock_price_tab(self):
        import stockPrice
        import datetime
        # the date string we get has the following format
        # 23 Dec 3:29pm
        dtFormat = "%d %b %I:%M%p"
        # loop through the symbols in the list and
        # fill current stock price into the table.
        for st in self.symList:
            nseObj = stockPrice.GetStockPrice(st, exchange='NSE')
            bseObj = stockPrice.GetStockPrice(st, exchange='BSE')
            try:
                (currNSEDate, currNSEPrice) = nseObj.get_stock_data()
                # convert the datetime string to python datetime object
                currNSEDate = datetime.datetime.strptime(currNSEDate, dtFormat)
                # need to set the year as we dont get 
                # the information from the string.
                # get the current year
                currYear = datetime.datetime.utcnow().year
                currNSEDate = currNSEDate.replace(year=2014)
            except:
                (currNSEDate, currNSEPrice) = (None,None)
            try:
                (currBSEDate, currBSEPrice) = bseObj.get_stock_data()
                currBSEDate = datetime.datetime.strptime(currBSEDate, dtFormat)
                # need to set the year as we dont get 
                # the information from the string.
                # get the current year
                currYear = datetime.datetime.utcnow().year
                currBSEDate = currBSEDate.replace(year=2014)
            except:
                (currBSEDate, currBSEPrice) = (None,None)
            # fill in the price info in the tables
            print st, currNSEDate, currNSEPrice, currBSEDate, currBSEPrice
            break