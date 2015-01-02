if __name__ == "__main__":
    import yhNews
    ynObj = yhNews.GetYahooNews()
    newsList = ynObj.get_news_url_list()

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
        'https://in.finance.yahoo.com/news/'

    def get_news_url_list(self):
        # get the urls to the news items
        import bs4
        import urllib2
        # get the page url where news items are listed
        stockNewsUrl = self.baseNewsUrl + 'category-stocks/'
        # soupify
        urlData = urllib2.urlopen(stockNewsUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # the news items are in the li tags, first get the
        # ul class associated with the news items.
        newsListUlTag = soup.findAll( \
            attrs={'class': "yom-mod yom-top-story"} )
        newsListLiTags = newsListUlTag[0].findAll('li')
        newsList = []
        for nl in newsListLiTags:
            try:
                currNL = nl.findAll('a')
                newsList.append( currNL[0]['href'] )
            except:
                continue
        return newsList