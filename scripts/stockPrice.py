class GetStockPrice(object):
    """
    A class to get the price of stocks at the current time.

    Right I'm using yahoo finance.
    """

    def __init__(self, stockSymbol, exchange='NSE'):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # set the base url for yahoo finance
        baseUrl = 'https://in.finance.yahoo.com/q?s='
        # set the extension in yahoo finance according to 
        # the exchange. currently we'll just have NSE and BSE
        if exchange == 'BSE':
            urlExt = '.BO'
        else:
            urlExt = '.NS'
        # url of the page with the stock info
        self.stockUrl = baseUrl + stockSymbol + urlExt

    def get_stock_data(self):
        # Now the urls are paginated so we need all the urls.
        # We'll keep them in a list.
        import bs4
        import urllib2
        # soupify
        urlData = urllib2.urlopen(self.stockUrl).read()
        soup = bs4.BeautifulSoup(urlData)