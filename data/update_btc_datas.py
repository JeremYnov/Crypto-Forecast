import numpy as np
import pandas as pd
import pandas_datareader as pd_dr
from config.mongo import Mongo
from datetime import datetime, timedelta

def update_datas( initialisation = True ):
    btc_collection = Mongo().getCollection("btc")
    if initialisation and btc_collection.find().count() == 0 :
        print('Initialisation')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', datetime.datetime(2015,1,1), datetime.datetime.now())
    elif initialisation:
        print('Already initialise')
        return
    else :
        print('Updating datas')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', datetime.today() - timedelta(days=1), datetime.today() ).iloc[[-1]]
    data = data.drop(["Adj Close"], axis=1)
    data.reset_index(inplace=True)
    data = data.rename(columns = {'Date':'_id'})            
    for column in data.columns :
        data[f"Predicted {column}"] = np.nan
    btc_collection.insert_many(data.to_dict('records'))
