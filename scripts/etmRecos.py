if __name__ == "__main__":
    import etmRecos
    etObj = etmRecos.GetEcTimesRecos()
    recosBaseUrl = etObj.get_recos_baseurl()
    artDict = etObj.get_articles(recosBaseUrl)


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
        # get the base url of the recommendations page
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
        print "Base URL not found"
        return None

    def get_articles(self, recosBaseUrl):
        # get the details of the recos
        import bs4
        import urllib2
        import datetime
        # check if the url is None, if so return empty dict
        if recosBaseUrl is None:
            print "URL is None"
            return {}
        # soupify
        urlData = urllib2.urlopen(recosBaseUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # get the actual urls for articles, they are under class eachStory
        etUrlIdTag = soup.findAll( \
            attrs={'class': "eachStory"} )
        urlDict = {}
        for etu in etUrlIdTag:
            try:
                currArtUrl = etu.find('a')['href']
                try:
                    currArtTimeStr = str(etu.find('time').string)
                    dtFmt = '%d %b %Y, %H:%M %p IST'
                    currTime = datetime.datetime.\
                                        strptime(currArtTimeStr,dtFmt)
                except:
                    # get today's date if we are not able to convert to
                    # datetime object.
                    print "couldn't retrieve date, using today's date"
                    currTime = datetime.date.today()
                currArtText = etu.find('a').get_text()
                # store data in dict
                urlDict[currArtUrl] = {}
                urlDict[currArtUrl]['date'] = currTime
                urlDict[currArtUrl]['text'] = currArtText
                urlDict[currArtUrl]['source'] = "Economic Times"
            except:
                print "curr article update failed"
                continue
        return urlDict