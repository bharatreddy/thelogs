class MongoUtils(object):
    """
    A class to store/create and retrieve data 
    from the MongoDB database
    """

    def __init__(self):
        import pymongo
        # set up connections to Mongo
        self.conn = pymongo.MongoClient()
        # Conect to the database and collections
        self.db = self.conn['LogBook']
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
            # self.newsColl.update( {'id':nd}, currDict, True )
            self.newsColl.save(currDict)

    def insert_recos(self, recosDict):
        # insert news items into the db
        # loop through the dict and insert
        # the news items
        for nd in recosDict.keys():
            currDict = recosDict[nd]
            # We'll have _id as the url to the news
            # or key here, so that we'll avoid 
            # duplicate newsarticle
            currDict['_id'] = nd
            # self.recosColl.update( {'id':nd}, currDict, upsert=False )
            self.recosColl.save(currDict)

    def get_news(self):
        # get news items from the db
        # which we got in the last 3-4 days
        # also limit the number of items to 20.
        newsArt = self.newsColl.find_one()
        return newsArt

    def close(self):
        # close connections to mongodb
        self.conn.close()