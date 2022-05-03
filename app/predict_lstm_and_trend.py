import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as pd_dr
import pymongo
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential, save_model, load_model

from tools.mongo_connector import Mongo
from script_update_btc_datas import update_datas


class Predict:
    def __init__(self, date):
        self.btc_columns = { '_id': 1, 'High': 1, 'Low': 1, 'Open': 1, 'Close': 1, 'Volume': 1 }
        # recuperation de mongo et de la collection btc
        mongo = Mongo()
        self.btc_collection = mongo.getCollection("btc")
        self.name_model_lstm = "model_ltsm"
        self.chunks_size = 90
        self.date = date
        # on ajoute la donnée de la journée
        try:
            update_datas(False)
        except:
            print("données déjà mis en base aujourd'hui")

    def get_data(self):
        # recuperation de toutes les datas du btc order by date
        btc_data = self.btc_collection.find({"_id": {"$lt": self.date}}, self.btc_columns).sort("_id", pymongo.ASCENDING)
        data_now = self.btc_collection.find({"_id": self.date}, self.btc_columns).sort("_id", pymongo.ASCENDING)
        # transformation des datas du btc en df
        self.data_training = pd.DataFrame(list(btc_data))
        data_now = pd.DataFrame(list(data_now))
        self.data_training = pd.concat([self.data_training, data_now], axis=0)
        # copy du df
        self.trend_training_data = self.data_training.copy()
        self.trend_training_data = self.trend_training_data.set_index("_id")
    

    def preprocessing_trend(self):
        # on recupere la derniere ligne du df qui est la data que l'on veut predire
        self.data_pred = self.trend_training_data.iloc[[len(self.trend_training_data) - 1]]
        # on recupere les autres lignes qui vont entrainer le modele
        self.trend_training_data = self.trend_training_data[:-1]

        #trend preprocessing
        trend_training_data_j1 = self.trend_training_data.shift(periods=1)
        #creation de la colonne tendance, dans laquelle on soustrait le prix du jour actuel au prix j-1
        self.trend_training_data['Diff_J+1'] = self.trend_training_data["Close"] / trend_training_data_j1["Close"]

        #suppression des lignes avec NaN (la premiere n'a pas de tendance vu qu'on a pas de jour precedent
        #on supprime la ligne plutot que de mettre une donnée fausse car il y'a 2192 lignes)
        self.trend_training_data.dropna(subset = ["Diff_J+1"], inplace=True)

        # on creer le x et y
        self.trend_training_x = self.trend_training_data.drop(columns=['Diff_J+1'])
        self.trend_training_y = self.trend_training_data['Diff_J+1']

        # on scale les données pour données une meilleure precision au model
        trend_scaler = MinMaxScaler( feature_range=(0,1) ) 
        self.trend_training_x = trend_scaler.fit_transform(self.trend_training_x)
        self.data_pred = trend_scaler.fit_transform(self.data_pred)

    def training_model_RandomForestRegressor(self):
        # on entraine le modele
        self.model = RandomForestRegressor()
        print("Debut de l'entrainement")
        self.model.fit(self.trend_training_x, self.trend_training_y)
        print("Fin de l'entrainement")    

    def predict_trend(self):
        # on fait la prediciton
        print("Debut de la prediction")
        self.trend_prediction = self.model.predict(self.data_pred)
        print("Fin de la prediction")

    def update_data_predict_trend(self):
        self.now = dt.datetime.now()
        query = {"_id": self.date}
        newvalues = { "$set": {"trend": self.trend_prediction[0]}}
        try:
            # on udpate la ligne du jours en ajoutant la colonne trend
            self.btc_collection.update_one(query, newvalues)
            print("update en base reussis")
        except:
            print("erreur à l'update en base")

    def processing_lstm(self):
        lstm_training_data = self.data_training.copy()
        lstm_training_data = lstm_training_data.set_index("_id")

        # on recupere un paquet de 90 lignes
        self.data_pred_lstm = lstm_training_data.iloc[len(lstm_training_data) - self.chunks_size: len(lstm_training_data)]
        # on recupere les autres lignes qui vont entrainer le modele
        lstm_training_data = lstm_training_data[:-self.chunks_size]
        
        # on supprime la premiere ligne car il n'ya pas de trend sur le premiere donnée
        lstm_training_data = lstm_training_data.iloc[1: , :]
        
        # on recupere les trend entrainement du df de trend_training_y
        self.trend_training = self.trend_training_y.iloc[:-self.chunks_size + 1]
        # on recupere les trend predict du df de trend_training_y
        trend_predict = self.trend_training_y.iloc[len(lstm_training_data): len(lstm_training_data) + (self.chunks_size -1)]

        # on recupere la donnée du jours en la passant en df qu'on avait creer dans les trends
        dict_pred = {"_id": self.date, "Diff_J+1": self.trend_prediction[0]}
        df_pred = pd.DataFrame(dict_pred, index=[0])
        df_pred = df_pred.set_index("_id")

        # on concat les des df pour avoir le paquet de 90
        trend_predict = pd.concat([trend_predict.to_frame(), df_pred], axis=0)

        # on ajoute les trends predit juste avant dans le df de training et le df qu'on veut predire
        lstm_training_data['Predicted Trend'] = self.trend_training
        self.data_pred_lstm['Predicted Trend'] = trend_predict

        # processing
        self.scaler = MinMaxScaler( feature_range=(0,1) )
        scaled_data = self.scaler.fit_transform( lstm_training_data ) 
        #Fragmente le dataset en plusieurs packets
        
        self.lstm_training_x, self.lstm_training_y = list(), list()

        # fragentation du x et y par packeks de self.chunks_size
        for x in range( self.chunks_size, len(scaled_data) ):
            self.lstm_training_x.append(scaled_data[x-self.chunks_size:x])
            self.lstm_training_y.append(scaled_data[x])

        # conversion en tableay numpy
        self.lstm_training_x, self.lstm_training_y = np.array(self.lstm_training_x), np.array(self.lstm_training_y)

    def save_model(self):
        # creation du model
        self.model = Sequential()

        self.model.add( LSTM(units=60, return_sequences=True, input_shape=(self.lstm_training_x.shape[1], 6)) )
        self.model.add( Dropout(0.2) )
        self.model.add( LSTM(units=80, return_sequences=True) )
        self.model.add( Dropout(0.3) ) 
        self.model.add( LSTM(units=120) )
        self.model.add( Dropout(0.4) ) 
        self.model.add( Dense(units=6) )

        self.model.summary()
        
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(self.lstm_training_x, self.lstm_training_y , epochs=30, batch_size=32, validation_split=0.1)
        # sauvegarde du model
        save_model(self.model, self.name_model_lstm)
    
    def load_model_lstm(self):
        # on teste la recuperation du modele, si il ne trouve pas la save, il entraine le model plus le sauvegarde et le load
        try :
            model = load_model(self.name_model_lstm)
        except :
            print("ce model n'a pas été sauvegarder, il faut donc l'entrainer puis le sauvegarder")
            self.save_model()
            model = load_model(self.name_model_lstm)
        return model

    def predict_lstm(self):
        # on load le model
        model = self.load_model_lstm()
        model_inputs = self.data_pred_lstm.values
        model_inputs = self.scaler.fit_transform(model_inputs)
        lstm_testing_x = list()
        lstm_testing_x.append(model_inputs)
        lstm_testing_x = np.array(lstm_testing_x)

        # on predit
        print("debut de la prediciton")
        self.prediction_prices = model.predict(lstm_testing_x)
        print(self.prediction_prices)
        print("fin de la prediciton")
        self.prediction_prices = self.scaler.inverse_transform(self.prediction_prices)
    
    def update_data_predict_ltsm(self):
        query = {"_id": self.date}
        newvalues = { "$set": {
            "Predicted High": float(self.prediction_prices[0][0]),
            "Predicted Low": float(self.prediction_prices[0][1]),
            "Predicted Open": float(self.prediction_prices[0][2]),
            "Predicted Close": float(self.prediction_prices[0][3]),
            "Predicted Volume": float(self.prediction_prices[0][4])
        }}
        try:
            # on udpate la ligne du jours en ajoutant la colonne trend
            self.btc_collection.update_one(query, newvalues)
            print("update en base reussis")
        except:
            print("erreur à l'update en base")

if __name__ == "__main__":
    now = dt.datetime.now()
    date = dt.datetime(
        int(now.strftime("%Y")), 
        int(now.strftime("%m")), 
        int(now.strftime("%d")), 
        0, 
        0
    )
    predict = Predict(date)
    predict.get_data()
    predict.preprocessing_trend()
    predict.training_model_RandomForestRegressor()
    predict.predict_trend()
    predict.update_data_predict_trend()
    predict.processing_lstm()
    # predict.save_model()
    predict.predict_lstm()
    predict.update_data_predict_ltsm()
