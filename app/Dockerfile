FROM python:3.8

RUN mkdir cryptoForecast
COPY requirements.txt /cryptoForecast/requirements.txt
RUN pip install -r /cryptoForecast/requirements.txt

CMD [ "python3", "/home/script_update_btc_datas.py", "True"]
