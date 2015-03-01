if __name__ == "__main__":
    import yhNews
    import mongoLib
    ynObj = yhNews.GetYahooNews()
    newsList = ynObj.get_news_url_list()
    artDict = ynObj.get_news_articles(newsList)
    mnObj = mongoLib.MongoUtils()
    mnObj.insert_news(artDict)
    mnObj.close()


class GetYahooNews(object):
    """
    A class to get the news from yahoo site.

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
        # set the base url for yahoo finance
        self.baseNewsUrl = \
        'https://in.finance.yahoo.com/'

    def get_news_url_list(self):
        # get the urls to the news items
        import bs4
        import urllib2
        # get the page url where news items are listed
        stockNewsUrl = self.baseNewsUrl + 'news/'#category-stocks/
        # soupify
        urlData = urllib2.urlopen(stockNewsUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # the news items are in the li tags, first get the
        # ul class associated with the news items.
        newsListTag = soup.findAll( \
            attrs={'class': "list-story"} )
        # Now we have a list of objects, work with them
        # individually and get the links
        newsListh4Tags = [ nh.findAll('h4') for nh in newsListTag ]
        newsList = []
        for nl in newsListh4Tags:
            try:
                currNL = nl[0].findAll('a')
                newsList.append( currNL[0]['href'] )
            except:
                continue
        return newsList

    def get_news_articles(self, articleList):
        # get the urls to the news items
        import bs4
        import urllib2
        import re
        import datetime
        rlvntArticles = {}
        for al in articleList:
            # get the full url of the page
            fullNewsUrl = self.baseNewsUrl + al
            # soupify
            try:
                urlData = urllib2.urlopen(fullNewsUrl).read()
                soup = bs4.BeautifulSoup(urlData)
                # the text is located in div with class labelled "entry-content"
                newsArtcleDiv = soup.findAll( \
                attrs={'id': "mediaarticlebody"} )
                # check for any content
                if len(newsArtcleDiv) == 0:
                    continue
                # get all the paragraph tags in the div
                newsArtclePTag =newsArtcleDiv[0].findAll('p', text=True)
                try:
                    timeTag = soup.findAll( \
                    attrs={'class': 'byline'} )
                    currTimeStr = timeTag[0].find('abbr', text=True)['title']
                    # remove unnecessary chars from datestr
                    currTimeStr = currTimeStr.replace( "T", "-" )
                    currTimeStr = currTimeStr.replace( "Z", "" )
                    dtFmt = '%Y-%m-%d-%H:%M:%S'
                    currTime = datetime.datetime.\
                            strptime(currTimeStr,dtFmt)
                except:
                    print "couldn't retrieve date, using today's date"
                    currTime = datetime.date.today()
                newsText = ''
                for nn in newsArtclePTag:
                    newsText += nn.get_text()
                    newsText += ' '
                # check if the any stock names/symbols
                # are found in the string.
                # first get the list of stocknames and symbols
                stockSyms, stockNames = self.get_stock_lists()
                stockData = stockSyms + stockNames
                # add some additional terms
                # stockData += ['shares', 'stocks', 'industry']
                if any(word in newsText for word in stockData):
                    rlvntArticles[fullNewsUrl] = {}
                    rlvntArticles[fullNewsUrl]['text'] = newsText
                    # get date from current obj, its not simple 
                    # to get datetime from python datetime obj
                    rlvntArticles[fullNewsUrl]['date'] = currTime
                    rlvntArticles[fullNewsUrl]['source'] = "Yahoo News"
                else:
                    continue
            except:
                print "couldn't get article text!"
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