if __name__ == "__main__":
    import createDB
    dbo = createDB.DbUtils()
    dbo.create_all_tables()
    dbo.close()

class DbUtils(object):
    """
    A utilities class to create the Logbook mysql Db and corresponding tables.
    """

    def __init__(self):
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='Logbook')
        self.cursor = self.conn.cursor()

    def create_all_tables(self):
        import mysql.connector
        # create the StockSymbols table
        stsymStr = """
                    CREATE TABLE StockSymbols(
                        stocksymbol VARCHAR(100) NOT NULL,
                        stockname VARCHAR(200) NOT NULL,
                        PRIMARY KEY (stocksymbol)
                        )
                    """
        self.cursor.execute(stsymStr)
        # create the StockPrices table
        stPrcStr = """
                    CREATE TABLE StockPrices(
                        stock_symbol VARCHAR(100) NOT NULL,
                        NSE_cost_per_unit FLOAT NULL,
                        NSE_datetime DATETIME NULL,
                        BSE_cost_per_unit FLOAT NULL,
                        BSE_datetime DATETIME NULL,
                        FOREIGN KEY (stock_symbol) REFERENCES StockSymbols(stocksymbol)
                        )
                    """
        self.cursor.execute(stPrcStr)
        # create the Users table
        stUsrStr = """
                    CREATE TABLE Users(
                        userid INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(120) NOT NULL UNIQUE,
                        pwdhash VARCHAR(100) NOT NULL,
                        PRIMARY KEY (userid)
                        )
                    """
        self.cursor.execute(stUsrStr)
        # create the TransactionTypes table
        sttrtypStr = """
                    CREATE TABLE TransactionTypes(
                        transaction_type_id INT NOT NULL,
                        transaction_type VARCHAR(10) NOT NULL,
                        PRIMARY KEY (transaction_type_id)
                        )
                    """
        self.cursor.execute(sttrtypStr)
        # create the stockTransactions table
        ststtrnStr = """
                    CREATE TABLE StockTransactions(
                        transaction_id INT NOT NULL AUTO_INCREMENT,
                        userid INT NOT NULL,
                        stock_symbol VARCHAR(100) NOT NULL,
                        date DATETIME NOT NULL,
                        transaction_type_id INT NOT NULL,
                        stock_exchange VARCHAR(20) NOT NULL,
                        quantity INT NOT NULL,
                        cost_per_unit FLOAT NOT NULL,
                        simulated VARCHAR(10) NULL,
                        PRIMARY KEY (transaction_id),
                        FOREIGN KEY (userid) REFERENCES Users(userid),
                        FOREIGN KEY (stock_symbol) REFERENCES StockSymbols(stocksymbol),
                        FOREIGN KEY (transaction_type_id) REFERENCES TransactionTypes(transaction_type_id)
                        )
                    """
        self.cursor.execute(ststtrnStr)
        self.conn.commit()

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.conn.close()