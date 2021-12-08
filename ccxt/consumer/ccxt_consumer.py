import os
from dotenv import load_dotenv
from json import loads
from pymongo import MongoClient
from kafka import KafkaConsumer

load_dotenv()

# connexion à la bdd
mongo_url = "mongodb://{username}:{password}@mongodb:27017".format(username=os.getenv('MONGO_ROOT_USERNAME'),
                                                                   password=os.getenv('MONGO_ROOT_PASSWORD'))
client = MongoClient(mongo_url)

# connexion à la database
database = client[os.getenv('MONGO_DATABASE')]

# creation des collections
collection_crypto = database['crypto']
collection_news = database['news']
collection_symbol = database['symbol']

# recuperation des collections
symbol_db = database.get_collection("symbol")
news_db = database.get_collection("news")
crypto_db = database.get_collection("crypto")

consumer = KafkaConsumer('crypto_raw',
                        bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVER')],
                        api_version=(0, 10, 1))

for ccxt_raw in consumer:
  crypto = loads(ccxt_raw.value.decode("utf-8"))
  if crypto["symbol"].split("/")[1] == "USD":
    already = False

    # on boucle sur tous les symbols enn base et on verifie si le symbol est déjà dans la base
    for symbol in symbol_db.find({}):
      if symbol["name"] == crypto["symbol"]:
        already = True

    # si il n'es pas dans la base on l'ajoute en base
    if not already :
      symbol_db.insert_one({"name": crypto["symbol"]})

    symbol = symbol_db.find_one({"name": crypto["symbol"]}) # recuperation du symbol crypto ex (BTC/USD)
    crypto_db.insert_one({
                          "date_time": crypto["datetime"],
                          "price": crypto["last"],
                          "symbol": symbol["_id"],
                          "high": crypto["high"],
                          "low": crypto["low"],
                          "average": crypto["average"]
                        }) #INSERTION CRYPTO
