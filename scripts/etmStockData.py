class GetStockData(object):
    """
    A class to get the data about stocks from Economic times.

    We'll crawl through and retreive data of stocks/companies 
    like Market Cap, P/E, Face Value and so on. Almost everything
    available on the economic times website.
    """

    def __init__(self):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # set the base url
        self.baseUrl = \
        'http://economictimes.indiatimes.com/markets/stocks/stock-quotes'
    
    