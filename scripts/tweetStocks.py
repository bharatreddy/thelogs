from tweepy.streaming import StreamListener
if __name__ == "__main__":
    import tweetStocks
    twts = tweetStocks.StockTweets()
    allStockNames = twts.get_stock_lists()
    actvStockNames = twts.get_stock_trans_list()
    print actvStockNames
    twts.get_stream_data(srchWords=actvStockNames[0])

class StockTweets(object):
    """
    A python class to get tweets about stocks using 
    the streaming API.
    """
    def __init__(self):
        #Import the necessary funcs from tweepy
        from tweepy.streaming import StreamListener
        from tweepy import OAuthHandler
        from tweepy import Stream
        # set the key and secret
        self.consumerKey = "8Ug3XPRlkM5oWka7l8dXF5WBl"
        self.consumerSecret = "zDhlhTMAFuAH8KTrR9R6zSm1h1BmDAtdW0VoAWeSWKCLr6s1Nf"
        self.accessToken = "1406261119-JDCMHDhDxDcO5sCdy1hxkCHkyLL0vz1Jm3vRCsv"
        self.accessSecret = "JXndVBLTaPqLf0oHxlD4c0NKmjBtRUPpISaKbUi3u4J4Q"
        # Handle Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener()
        auth = OAuthHandler(self.consumerKey, self.consumerSecret)
        auth.set_access_token(self.accessToken, self.accessSecret)
        self.stream = Stream(auth, l)

    def get_stock_lists(self):
        # get a list of all the stocks in our database
        import pandas
        import mysql.connector
        conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
        qryStockNames = "SELECT stocksymbol, stockname FROM StockSymbols"
        stockListDF = pandas.read_sql( qryStockNames, conn )
        stockNames = stockListDF['stockname'].tolist()
        return stockNames

    def get_stock_trans_list(self):
        # get a list of all the stocks in our database
        import pandas
        import mysql.connector
        conn = mysql.connector.Connect(host='localhost',user='root',\
                        password='',database='Logbook')
        qryStockNames = "SELECT DISTINCT stockname FROM stockTransactions"+\
        " INNER JOIN stockSymbols ON stock_symbol=stocksymbol;"
        stockListDF = pandas.read_sql( qryStockNames, conn )
        stockNames = stockListDF['stockname'].tolist()
        return stockNames

    def get_stream_data(self, srchWords=[]):
        # use the stream to get data about key words
        streamData = \
        self.stream.filter(track=srchWords)
        print streamData


class StdOutListener(StreamListener):
    """
    This is a basic listener that prints received tweets to stdout.
    """

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status