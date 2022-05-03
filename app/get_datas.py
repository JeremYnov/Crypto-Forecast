import datetime as dt

from predict_lstm_and_trend import Predict


date = dt.datetime(2022, 1, 1, 0, 0)
end_date = dt.datetime.now()
delta = dt.timedelta(days=1)

while date <= end_date:
    predict = Predict(date)
    predict.get_data()
    predict.preprocessing_trend()
    predict.training_model_RandomForestRegressor()
    predict.predict_trend()
    predict.update_data_predict_trend()
    predict.processing_lstm()
    predict.predict_lstm()
    predict.update_data_predict_ltsm()
    date += delta
    