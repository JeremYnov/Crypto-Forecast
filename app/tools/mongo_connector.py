import os
from pymongo import MongoClient
from dotenv import load_dotenv

class Mongo:
    def __init__(self):
        load_dotenv()
        self.client = MongoClient(os.getenv("MONGO_URL"))
        # database connection
        self.database = self.client[os.getenv("MONGO_DB_NAME")]
    
    def getCollection(self, collection_name):
        return self.database.get_collection(collection_name)