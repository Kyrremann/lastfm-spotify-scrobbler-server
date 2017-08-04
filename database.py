import pymongo

class Database:
    """A simple MongoDB class for working with the
    Spotify and Last.fm credentials that we store

    Args:
        uri (str):
        database (str):
        collection (str):
    """

    def __init__(self, uri, database, collection):
        self.client = pymongo.MongoClient(uri)
        self.database = client[database]
        self.collection = db[collection]

    def update_credentials(self, user_id, data):
        self.collection.update_one({'_id': ObjectId(self.document_id)}, {'$set': data})

    def find_credentials(self, document_id):
        return self.collection.find_one(document_id)
