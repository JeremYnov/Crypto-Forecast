import sys
import numpy as np
import pandas as pd
import pandas_datareader as pd_dr
from datetime import datetime as dt

from tools.mongo_connector import Mongo


def update_datas(initialisation):
    btc_collection = Mongo().getCollection("btc")

    if initialisation and btc_collection.count_documents({}) == 0 :
        print('Initialisation')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', dt(2015,1,1), dt.now())
    elif initialisation:
        print('Already initialise')
        return
    else:
        print('Updating datas')
        data = pd_dr.DataReader( 'BTC-USD', 'yahoo', dt.today() - dt.timedelta(days=1), dt.today() ).iloc[[-1]]

    data = data.drop(["Adj Close"], axis=1)
    data.reset_index(inplace=True)
    data = data.rename(columns = {'Date':'_id'})
            
    for column in data.columns :
        data[f"Predicted {column}"] = np.nan

    btc_collection.insert_many(data.to_dict('records'))

if __name__ == "__main__":
    initialisation = bool(sys.argv[1])
    update_datas(initialisation)