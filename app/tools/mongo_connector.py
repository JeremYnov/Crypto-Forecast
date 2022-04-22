from pymongo import MongoClient
import os
from dotenv import load_dotenv

class Mongo:
    def __init__(self):
        load_dotenv()
        self.client = MongoClient(os.getenv("MONGO_URL"))
        # database connection
        self.database = self.client[os.getenv("MONGO_DB_NAME")]
    
    def getCollection(self, collection):
        # collections creation
        text_data = self.database[collection]

        # get collections
        text_data_db = self.database.get_collection(collection)
        return text_data_db