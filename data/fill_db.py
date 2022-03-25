from config.mongo import Mongo
import pandas as pd
import datetime as dt
import pandas_datareader as pd_dr
import numpy as np

def insert_data_yahoo():
    
    data = pd_dr.DataReader( 'BTC-USD', 'yahoo', dt.datetime(2015,1,1), dt.datetime.now())
    data = data.drop(["Adj Close"], axis=1)
    data.reset_index(inplace=True)
    data = data.rename(columns = {'Date':'_id'})
    print(data.columns)
    for column in data.columns :
        data[f"Predicted {column}"] = np.nan

    mongo = Mongo()
    
    btc_collection = mongo.getCollection("btc")
    # btc_collection.remove()
    btc_collection.insert_many(data.to_dict('records'))