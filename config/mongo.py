from pymongo import MongoClient
import os
from dotenv import load_dotenv

class Mongo:
    def __init__(self):
        load_dotenv()
        self.client = MongoClient(f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@mongodb:27017")
        # database connection
        self.database = self.client[os.getenv("MONGO_DATABASE")]
    
    def getCollection(self, collection):
        # collections creation
        text_data = self.database[collection]

        # get collections
        text_data_db = self.database.get_collection(collection)
        return text_data_db