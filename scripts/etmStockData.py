if __name__ == "__main__":
    import etmStockData
    etObj = etmStockData.GetStockData()
    tickerUrlList = etObj.get_ticker_urls()
    print tickerUrlList

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
    
    def get_ticker_urls(self):
        # Now there are a large number of companies and each company
        # is listed according to alphabets. In this function we'll 
        # get the urls of pages which show the companies by alphabets.
        import string
        # get a list of lower case alphabets
        tickList = list(string.ascii_lowercase)
        # there are also the digits 1-9 in the ticker list
        tickList += [ str(n) for n in range(1,10) ]
        urlList = []
        for ch in tickList:
            urlList.append( self.baseUrl + "?ticker=" + ch )
        return urlList