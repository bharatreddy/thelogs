if __name__ == "__main__":
    import createFrndDB
    dbo = createFrndDB.DbUtils()
    dbo.create_all_frnd_tables()
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

    def create_all_frnd_tables(self):
        import mysql.connector
        # create the Friends table
        frStr = """
            CREATE TABLE Friends(
                user_id INT NOT NULL,
                friend_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(userid),
                FOREIGN KEY (friend_id) REFERENCES Users(userid)
                )
            """
        self.cursor.execute(frStr)
        # create the FriendRequests table
        frReqStr = """
            CREATE TABLE FriendRequests(
                user_id INT NOT NULL,
                friend_id INT NOT NULL,
                request_date DATETIME NOT NULL,
                approved VARCHAR(20) NOT NULL,
                approved_date DATETIME NULL,
                FOREIGN KEY (user_id) REFERENCES Users(userid),
                FOREIGN KEY (friend_id) REFERENCES Users(userid)
                )
            """
        self.cursor.execute(frReqStr)
        self.conn.commit()

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.conn.close()