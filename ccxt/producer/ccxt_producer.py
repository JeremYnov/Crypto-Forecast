import ccxt
import os
from dotenv import load_dotenv
from json import dumps
from kafka import KafkaProducer
from time import sleep

load_dotenv()

producer = KafkaProducer(
  bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVER'),
  value_serializer=lambda x: dumps(x).encode('utf-8')
)

binance = ccxt.binanceus()

while True:
  try:
    tickers = binance.fetch_tickers()

    for ticker in tickers.values():
      producer.send('crypto_raw', ticker)
  except:
    print('ooops')

  sleep(20)
