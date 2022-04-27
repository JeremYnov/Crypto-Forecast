from flask import Flask, request
from tools.mongo_connector import Mongo
import json
from bson import json_util
import os

app = Flask(__name__)



mongo = Mongo()
btc_collection = mongo.getCollection("btc")

btc_columns = { '_id':1, 'High':1, 'Low':1, 'Open':1, 'Close':1, 'Volume':1 }
pred_columns = { '_id':1, 'Predicted High':1, 'Predicted Low':1, 'Predicted Open':1, 'Predicted Close':1, 'Predicted Volume':1 }

@app.route('/docs', methods=['GET'])
def docs():
    try:
        response = btc_collection.find({}).limit(int( request.args.get('pages') )) 
    except TypeError:
        response = btc_collection.find({})
    return json.dumps( list(response), default=json_util.default), 200

@app.route('/btcPrice', methods=['GET'])
def btcPrice():
    try:
        response = btc_collection.find({},btc_columns).limit(int( request.args.get('pages') ))
    except TypeError:
        response = btc_collection.find({},btc_columns)
    return json.dumps( list(response), default=json_util.default), 200

@app.route('/predPrice', methods=['GET'])
def predPrice():
    try:
        response = btc_collection.find({},pred_columns).limit(int( request.args.get('pages') ))
    except TypeError:
        response = btc_collection.find({},pred_columns)
    return json.dumps( list(response), default=json_util.default), 200

@app.route('/lastRow', methods=['GET'])
def lastRow():
    response = btc_collection.find().sort("_id", -1).limit(1)
    return json.dumps( list(response), default=json_util.default), 200

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

'''
route 1 : Retourner toutes les valeurs de la DB
route 2 : retourner vrai prix btc + Date
route 3 : retourner prediction + date
route 4 : retourner que dernière prédiction

TODO : Ajouter la tendance dans le Db
'''

if __name__ == "__main__":
	# app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)