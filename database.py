import pymongo
from bson import ObjectId

class Database:
    """A simple MongoDB class for working with the
    Spotify and Last.fm credentials that we store

    Args:
        uri (str):
        database (str):
        collection (str):
    """

    def __init__(self, uri, database_name, collection):
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database_name]
        self.collection = self.database[collection]

    def update_credentials(self, document_id, data):
        self.collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})

    def find_credentials(self, document_id):
        return self.collection.find_one({'_id': ObjectId(document_id)})
