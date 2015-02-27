if __name__ == "__main__":
    import etmNews
    etObj = etmNews.GetEcTimesRecos()
    urlDict = etObj.get_urls()
    newsUrl = ''
    if 'News' in urlDict:
        newsUrl = urlDict['News']
    etObj.get_url_data(newsUrl)


class GetEcTimesRecos(object):
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