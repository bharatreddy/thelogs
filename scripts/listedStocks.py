class GetListedStocks(object):
    """
    A class to get all the listed stocks in NSE and BSE.
    Right now I'm getting data from rediff.
    """

    def __init__(self):
        import string
        # get the base urls from rediff for both bse and nse
        self.baseUrlBse = 'http://money.rediff.com/companies/'
        self.baseUrlNse = 'http://money.rediff.com/companies/nseall/'
        # the stock names are order by alphabets
        alphabetList = string.ascii_lowercase
        for j in alphabetList:
            print j