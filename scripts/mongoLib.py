if __name__ == "__main__":
    import mongoLib
    mnObj = mongoLib.MongoUtils()
    mnObj.insert_news()

class MongoUtils(object):
    """
    A class to store/create and retrieve data 
    from the MongoDB database
    """

    def __init__(self):
        import pymongo
        # set up connections to Mongo
        conn = pymongo.MongoClient()
        # Conect to the database and collections
        self.db = conn['LogBook']
        self.newsColl = self.db['News']
        self.recosColl = self.db['Recos']

    def insert_news(self, newsDict):
        # insert news items into the db
        # loop through the dict and insert
        # the news items
        for nd in newsDict.keys():
            currDict = newsDict[nd]
            # We'll have _id as the url to the news
            # or key here, so that we'll avoid 
            # duplicate newsarticle
            currDict['_id'] = nd
            self.newsColl.update(currDict, upsert=True)
            