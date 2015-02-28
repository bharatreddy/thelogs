if __name__ == "__main__":
    import etmRecos
    etObj = etmRecos.GetEcTimesRecos()
    recosBaseUrl = etObj.get_recos_baseurl()
    print recosBaseUrl
    # newsUrl = ''
    # if 'News' in urlDict:
    #     newsUrl = urlDict['News']
    # etObj.get_url_data(newsUrl)


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

    def get_recos_baseurl(self):
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
        # get the url of Recos, start with getting nav bar 
        etUrlTag = etUrlNavTag[0].findAll('a')
        # Check if the term Recos is present in the list
        recosBaseUrl = None
        for etu in etUrlTag:
            if ("Recos" in etu['href']) or ("recos" in etu['href']):
                return self.baseNewsUrl + etu['href']
        # If url is not found
        return None
