class GetListedStocks(object):
    """
    A class to get all the listed stocks in NSE and BSE.
    Right now I'm getting data from rediff.
    """

    def __init__(self):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # get the base urls from rediff
        self.baseUrl = 'http://money.rediff.com/companies/nseall/'

    def get_all_urls(self):
        # Now the urls are paginated so we need all the urls.
        # We'll keep them in a list.
        import bs4
        import urllib2
        # soupify
        urlData = urllib2.urlopen(self.baseUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # the pagination is present in the table with 
        # the class named "pagination-container-company"
        paginationTab = soup.findAll( \
            attrs={'class': "pagination-container-company"} )
        pageTags = paginationTab[0].findAll('td')
        pageText = pageTags[0].text
        # find max number of stocks listed.
        maxStocks = \
        max( [int(pt) for pt in pageText.split() if pt.isdigit()] )
        # now make a list of the new urls
        urlList = [ self.baseUrl ]
        startPage = 200
        while startPage < maxStocks:
            newUrlText = self.baseUrl + str(startPage+1) + "-" + str(startPage+200)
            urlList.append(newUrlText)
            startPage += 200
        return urlList

    def get_stock_symbols(self):
        # we'll use BeautifulSoup for scraping rediff
        import bs4
        import urllib2
        # we'll loop through the td tags and retreive the info
        # Here the even numbered tags have the company info
        # the odd numbered tags have company symbol, so we need
        # take that into account. Store the results in a dict
        # get a list of all the urls associated
        allUrlsList = self.get_all_urls()
        # loop through each url and soupify
        for stUrl in allUrlsList:
            urlData = urllib2.urlopen(stUrl).read()
            soup = bs4.BeautifulSoup(urlData)
            # the stocks are listed in the "dataTable" table
            stocksTab = soup.findAll(attrs={'class': "dataTable"})
            # the <td> tags have the company information
            for stabs in stocksTab:
                tdTags = stabs.findAll('td')
                for n, t in enumerate(tdTags):
                    stockDict = {}
                    currText = t.text
                    currText = ' '.join(currText.split())
                    stockDict['name'] = currText
                    if n%2 == 0 :
                        symbolText = tdTags[n+1].text
                        stockDict['symbol'] = symbolText
                        # update the sql table
                        self.popStockSymTab(stockDict)
        return "Done updating the table"

    def popStockSymTab(self, stockDict):
        # populate the stock symbols tab
        query = ("INSERT INTO StockSymbols "
               " (stocksymbol, stockname) "
               " VALUES (%s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   stocksymbol=VALUES(stocksymbol), "
               "   stockname=VALUES(stockname) ")
        params = (
            stockDict["symbol"], 
            stockDict["name"])
        self.cursor.execute(query, params)
        self.conn.commit()