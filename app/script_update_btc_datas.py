import sys
from tools.mongo_connector import Mongo
import pandas as pd
from datetime import datetime as dt, timedelta
import pandas_datareader as pd_dr
import numpy as np

def update_datas(initialisation):
    
    today = dt.today()
    mongo = Mongo()
    btc_collection = mongo.getCollection("btc")

    if initialisation and btc_collection.count_documents({}) == 0 :
        print('Initialisation')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', dt(2015,1,1), dt.now())
    elif initialisation:
        print('Already initialise')
        return
    else :
        print('Updating datas')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', today - timedelta(days=1), today ).iloc[[-1]]

    data = data.drop(["Adj Close"], axis=1)
    data.reset_index(inplace=True)
    data = data.rename(columns = {'Date':'_id'})
            
    for column in data.columns :
        data[f"Predicted {column}"] = np.nan

    btc_collection.insert_many(data.to_dict('records'))

if __name__ == "__main__":
    initialisation = bool(sys.argv[1])
    update_datas(initialisation)