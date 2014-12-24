if __name__ == "__main__":
    import fillStockPriceTab
    stp = fillStockPriceTab.FillStockPriceTable()

class FillStockPriceTable(object):
    """
    A class to fill in the stock prices table,
    with current price details from yahoo finance.
    """

    def __init__(self):
        import string
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()
        # get a list of all symbols in StockSymbols table
        qrySyms = ("""
            SELECT DISTINCT stocksymbol
            FROM StockSymbols
            """)
        self.cursor.execute(qrySyms)
        self.symList = [s[0] for s in self.cursor]