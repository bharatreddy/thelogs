if __name__ == "__main__":
    import etmNews
    etObj = etmNews.GetEcTimesNews()
    urlDict = etObj.get_urls()
    # etObj.get_news_articles(newsList)


class GetEcTimesNews(object):
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
        # set the base url for economic times
        self.baseNewsUrl = \
        'http://economictimes.indiatimes.com/'

    def get_urls(self):
        # get the urls to the news items
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
            urlDict[etu.get_text()] = etu['href']
        return urlDict