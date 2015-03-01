if __name__ == "__main__":
    import mongoLib
    mnObj = mongoLib.MongoUtils()

class MongoUtils(object):
    """
    A class to store/create and retrieve data 
    from the MongoDB database
    """

    def __init__(self):
        import pymongo
        # set up connections to MongoDB
        conn = pymongo.Connection()
        # Conect to the database and collections
        self.db = conn['LogBook']
        self.newsColl = self.db['News']
        self.recosColl = self.db['Recos']