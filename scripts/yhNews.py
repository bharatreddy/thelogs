if __name__ == "__main__":
    import yhNews
    nwObj = yhNews.GetYahooNews()

class GetYahooNews(object):
    """
    A class to get the news from yahoo site.

    We'll get news from those articles where there was
    a mention of one of the stocks listed in our db.
    """

    def __init__(self, stockSymbol, exchange='NSE'):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # set the base url for yahoo finance
        self.baseNewsUrl = \
        'https://in.finance.yahoo.com/news/category-stocks/'

    def get_news_list(self):
        # Now the urls are paginated so we need all the urls.
        # We'll keep them in a list.
        import bs4
        import urllib2
        # soupify
        urlData = urllib2.urlopen(self.stockUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # the time and cost info is associated with a class
        # with tags yfi_rt_quote_summary_rt_top, sigfig_promo_0
        stockDivs = soup.findAll( \
            attrs={'class': "yfi_rt_quote_summary_rt_top"} )
        stockPriceTags = stockDivs[0].findAll('span')
        currStockPrice = stockPriceTags[0].text
        currTime = stockPriceTags[-1].text
        return currTime, currStockPrice