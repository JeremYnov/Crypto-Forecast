from predict_lstm_and_trend import Predict
import datetime as dt

date = dt.datetime(2022, 1, 1, 0, 0)
end_date = dt.datetime.now()
delta = dt.timedelta(days=1)

print(type(date))
print(type(end_date))

while date <= end_date:
    print(date)

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

    date += delta
    