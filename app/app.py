from flask import Flask, request
from tools.mongo_connector import Mongo
import json

app = Flask(__name__)

mongo = Mongo()
btc_collection = mongo.getCollection("btc")

btc_columns = { '_id', 'High', 'Low', 'Open', 'Close', 'Volume' }
pred_columns = { '_id', 'Predicted High', 'Predicted Low', 'Predicted Open', 'Predicted Close', 'Predicted Volume' }

@app.route('/docs', methods=['GET'])
def docs():
    response = btc_collection.find({}).limit(request.args[0]) if request.args[0] else btc_collection.find({})
    return json.dumps(response), 200

@app.route('/btcPrice', methods=['GET'])
def btcPrice():
    response = btc_collection.find(btc_columns).limit(request.args[0]) if request.args[0] else btc_collection.find(btc_columns)
    return json.dumps(response), 200

@app.route('/predPrice', methods=['GET'])
def predPrice():
    response = btc_collection.find(pred_columns).limit(request.args[0]) if request.args[0] else btc_collection.find(pred_columns)
    return json.dumps(response), 200

@app.route('/lastRow', methods=['GET'])
def predPrice():
    response = btc_collection.find().sort({'_id':-1}).limit(1)
    return json.dumps(response), 200

'''
route 1 : Retourner toutes les valeurs de la DB
route 2 : retourner vrai prix btc + Date
route 3 : retourner prediction + date
route 4 : retourner que dernière prédiction

TODO : Ajouter la tendance dans le Db
'''