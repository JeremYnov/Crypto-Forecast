from matplotlib.pyplot import title
import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
from datetime import date
from PIL import Image

today = date.today()

# creating a single-element container.
placeholder = st.empty()

# Request API URL 
response = requests.get("http://app:5000/btcPrice").json()
df = pd.DataFrame(response)

pred_response = requests.get("http://app:5000/predPrice").json()
pred_df = pd.DataFrame(pred_response)

# Create candlestick chart 
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))

predicted_fig = go.Figure()
predicted_fig.add_trace(go.Candlestick(x=pred_df['Date'], open=pred_df['Open'], high=pred_df['High'], low=pred_df['Low'], close=pred_df['Close']))

#Display chart
st.header("Bitcoin prices from day 1")
st.plotly_chart(fig)

# # TODO (change request url) Request API URL 
# pred_response = requests.get("http://app:5000/btcPrice").json()
# pred_df = pd.DataFrame(pred_response)

while True: 

    with placeholder.container():
        binance_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        binance_response = requests.get(binance_url).json()
        binance_df = pd.DataFrame(binance_response['bpi']['USD'], index=[0])
        
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)
        
        
        if binance_df['rate_float'].values[0] < pred_df.iloc[-1:]['Close'].values[0]:
            image = Image.open('soleil.png')
        else: 
            image = Image.open('pluie.png')

        # print(binance_df['rate_float'])
        # print(pred_df.iloc[-1:]['Close'])
        # if binance_df['rate_float'] < pred_df.iloc[-1:]['Close']:
        #     image = Image.open('interface/soleil.png')
        # else:
        #     image = Image.open('interface/pluie.png')

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="BTC Price ₿/＄", value= round( binance_df['rate_float'] ,3))
        # kpi2.metric(label="Predicted close Price", value= binance_df['rate_float'] )
        kpi2.image(image)
        kpi3.metric(label="Predicted close Price", value= round( pred_df.iloc[-1:]['Close'], 3) )
        
        time.sleep(50)
    #placeholder.empty()