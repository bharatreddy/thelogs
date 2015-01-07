if __name__ == "__main__":
    import createDB
    dbo = createDB.DbUtils()
    # dbo.create_main_tables()
    dbo.create_innings_tables()
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

    def create_main_tables(self):
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

        # create the Match table
        mtchStr = """
                    CREATE TABLE Game(
                        Id INT NOT NULL,
                        MatchDate DATETIME NOT NULL,
                        Type VARCHAR(50) NOT NULL,
                        Venue VARCHAR(100) NULL,
                        Competition VARCHAR(100),
                        Overs FLOAT,
                        PRIMARY KEY (Id)
                        )
                    """
        self.cursor.execute(mtchStr)
        # create the Toss table
        tossStr = """
                    CREATE TABLE Toss(
                        MatchId INT NOT NULL,
                        Winner VARCHAR(100) NOT NULL,
                        Decision VARCHAR(50) NOT NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(tossStr)
        # create the Teams table
        teamsStr = """
                    CREATE TABLE Teams(
                        MatchId INT NOT NULL,
                        Team1 VARCHAR(100) NOT NULL,
                        Team2 VARCHAR(100) NOT NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(teamsStr)
        # create the Umpires table
        umpiresStr = """
                    CREATE TABLE Umpires(
                        MatchId INT NOT NULL,
                        Umpire1 VARCHAR(100) NOT NULL,
                        Umpire2 VARCHAR(100) NOT NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(umpiresStr)
        # create the PlayerOfMatch table
        playerOfMatchStr = """
                    CREATE TABLE PlayerOfMatch(
                        MatchId INT NOT NULL,
                        Player VARCHAR(100) NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(playerOfMatchStr)
        # create the Outcome table
        outComeStr = """
                    CREATE TABLE Outcome(
                        MatchId INT NOT NULL,
                        Winner VARCHAR(100) NULL,
                        Innings INT NULL,
                        Runs INT NULL,
                        Wickets INT NULL,
                        Result VARCHAR(50) NULL,
                        Eliminator VARCHAR(100) NULL,
                        Method VARCHAR(50) NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(outComeStr)
        self.conn.commit()

    def create_innings_tables(self):
        import mysql.connector
        # create the Innings table
        innStr = """
                    CREATE TABLE Innings(
                        MatchId INT NOT NULL,
                        InningsNum INT NOT NULL,
                        Team VARCHAR(50) NOT NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(innStr)
        # create the Deliveries table 
        delStr = """
                    CREATE TABLE Deliveries(
                        MatchId INT NOT NULL,
                        InnNum INT NOT NULL,
                        Over FLOAT NULL,
                        Batsman VARCHAR(100) NULL,
                        NonStriker VARCHAR(100) NULL,
                        Bowler VARCHAR(100) NULL,
                        BatsmanRuns INT NULL,
                        ExtraRuns INT NULL,
                        NonBoundary INT NULL,
                        Substitution VARCHAR(200) NULL,
                        Wicket VARCHAR(10) NULL,
                        WicketFielder VARCHAR(100) NULL,
                        WicketKind VARCHAR(100) NULL,
                        WicketPlayerOut VARCHAR(100) NULL,
                        Extra VARCHAR(100) NULL,
                        FOREIGN KEY (MatchId) REFERENCES Game(Id)
                        )
                    """
        self.cursor.execute(delStr)
        self.conn.commit()

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.conn.close()