class GetListedStocks(object):
    """
    A class to get all the listed stocks in NSE and BSE.
    Right now I'm getting data from rediff.
    """

    def __init__(self):
        import string
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
        # pageTags = pageTags.findAll('a').text
        print pageTags


    def get_stock_symbols(self):
        # we'll use BeautifulSoup for scraping rediff
        import bs4
        import urllib2
        # soupify
        urlData = urllib2.urlopen(self.baseUrl).read()
        soup = bs4.BeautifulSoup(urlData)
        # the stocks are listed in the "dataTable" table
        stocksTab = soup.findAll(attrs={'class': "dataTable"})
        # the <td> tags have the company information
        tdTags = stocksTab[0].findAll('td')
        # loop through the td tags and retreive the info
        # Here the even numbered tags have the company info
        # the odd numbered tags have company symbol, so we need
        # take that into account. Store the results in a dict
        stockDict = {}
        for n, t in enumerate(tdTags):
            currText = t.text
            currText = ' '.join(currText.split())
            if n%2 == 0 :
                symbolText = tdTags[n+1].text
                stockDict[currText] = symbolText