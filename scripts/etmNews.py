if __name__ == "__main__":
    import etmNews
    import mongoLib
    etObj = etmNews.GetEcTimesNews()
    urlDict = etObj.get_urls()
    newsUrl = ''
    if 'News' in urlDict:
        newsUrl = urlDict['News']
    artDict = etObj.get_url_data(newsUrl)
    mnObj = mongoLib.MongoUtils()
    mnObj.insert_news(artDict)
    mnObj.close()


class GetEcTimesNews(object):
    """
    A class to get the news from economic times.

    We'll get news from those articles where there was
    a mention of one of the stocks listed in our db.
    """

    def __init__(self):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # set the base url for economic times
        self.baseNewsUrl = \
        'http://economictimes.indiatimes.com/'

    def get_urls(self):
        # get the urls to different menu items
        import bs4
        import urllib2
        # get the url with all the links like News, Recos etc
        infoUrl = self.baseNewsUrl + 'markets/stocks/'
        # soupify 
        urlData = urllib2.urlopen(infoUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # get the actual url of the news website
        etUrlNavTag = soup.findAll( \
            attrs={'id': "subSecNav"} )
        etUrlTag = etUrlNavTag[0].findAll('a')
        urlDict = {}
        for etu in etUrlTag:
            urlDict[etu.get_text()] = self.baseNewsUrl + etu['href']
        return urlDict

    def get_url_data(self, newsUrl):
        # get required data from a url
        import bs4
        import urllib2
        import datetime
        # get the list of news articles
        if newsUrl == '':
            return None
        # soupify 
        urlData = urllib2.urlopen(newsUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # get the actual url of the news website
        urlListDiv = soup.findAll( \
            attrs={'class': "eachStory"} )
        stockSyms, stockNames = self.get_stock_lists()
        stockData = stockSyms + stockNames
        # add some additional terms
        # stockData += ['shares', 'stocks', 'industry']
        # have a dict of relavant articles
        rlvntArticles = {}
        for ud in urlListDiv:
            try:
                udTag = ud.findAll('a')
                currUrl = self.baseNewsUrl + udTag[0]['href']
                # soupify the current url
                currUrlData = urllib2.urlopen(currUrl).read()
                currSoup = bs4.BeautifulSoup(currUrlData)
                # get the actual url of the news website
                currUrlTextDiv = currSoup.findAll( \
                    attrs={'class': "artText"} )
                currArtTitle = currSoup.find( \
                    attrs={'class': "title"} )
                # get time and convert it into datetime obj
                try:
                    currTime = str(currSoup.find( \
                        attrs={'class': "byline"} ).get_text())
                    if '|' in currTime:
                        currTime = currTime.split( '| ', 1 )[1]
                    dtFmt = '%d %b, %Y, %H.%M%p IST'
                    currTime = datetime.datetime.\
                                strptime(currTime,dtFmt)
                except:
                    # get today's date if we are not able to convert to
                    # datetime object.
                    print "couldn't retrieve date, using today's date"
                    currTime = datetime.date.today()
                currText = currUrlTextDiv[0].get_text()
                # if no text present, skip the article
                if len(currText) <= 2:
                    continue
                if any(word in currText for word in stockData):
                    rlvntArticles[currUrl] = {}
                    rlvntArticles[currUrl]['text'] = currText
                    rlvntArticles[currUrl]['date'] = currTime
                    rlvntArticles[currUrl]['title'] = currArtTitle.get_text()
                    rlvntArticles[currUrl]['source'] = "Economic Times"
                else:
                    continue
            except:
                print "missed curr article"
                continue
        return rlvntArticles

    def get_stock_lists(self):
        # get a list of all the stocks in our database
        import pandas
        import mysql.connector
        conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
        qryStockNames = "SELECT stocksymbol, stockname FROM StockSymbols"
        stockListDF = pandas.read_sql( qryStockNames, conn )
        stockNames = stockListDF['stockname'].tolist()
        stockSyms = stockListDF['stocksymbol'].tolist()
        return stockSyms, stockNames

    def get_stock_trans_list(self):
        # get a list of all active stocks in our database
        import pandas
        import mysql.connector
        conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
        qryStockNames = "SELECT DISTINCT stockname FROM stockTransactions"+\
        " INNER JOIN stockSymbols ON stock_symbol=stocksymbol;"
        stockListDF = pandas.read_sql( qryStockNames, conn )
        stockNames = stockListDF['stockname'].tolist()
        return stockNames