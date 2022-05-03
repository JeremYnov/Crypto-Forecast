import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import requests
import time
from PIL import Image


# creating a single-element container.
placeholder = st.empty()

# Create candlestick chart for bitcoin predictions
pred_df = pd.DataFrame(
    requests.get("http://app:5000/predPrice").json()
)
st.header("Bitcoin prediction prices")
st.plotly_chart(go.Figure().add_trace(
    go.Candlestick(
        x=pred_df['Date'], 
        open=pred_df['Predicted Open'], 
        high=pred_df['Predicted High'], 
        low=pred_df['Predicted Low'], 
        close=pred_df['Predicted Close']
)))

# Create candlestick chart for bitcoin
btcPrice_df = pd.DataFrame(
    requests.get("http://app:5000/btcPrice").json()
)
st.header("Bitcoin prices")
st.plotly_chart(go.Figure().add_trace(go.Candlestick(
    x=btcPrice_df['Date'], 
    open=btcPrice_df['Open'], 
    high=btcPrice_df['High'], 
    low=btcPrice_df['Low'], 
    close=btcPrice_df['Close']
)))

# # TODO (change request url) Request API URL 
# pred_response = requests.get("http://app:5000/btcPrice").json()
# pred_df = pd.DataFrame(pred_response)

while True: 
    with placeholder.container():
        binance_df = pd.DataFrame(requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json").json()['bpi']['USD'], 
            index=[0]
        )        
        
        if binance_df['rate_float'].values[0] < pred_df.iloc[-1:]['Predicted Close'].values[0]:
            image = Image.open('soleil.png')
        else: 
            image = Image.open('pluie.png')

        # print(binance_df['rate_float'])
        # print(pred_df.iloc[-1:]['Close'])
        # if binance_df['rate_float'] < pred_df.iloc[-1:]['Close']:
        #     image = Image.open('interface/soleil.png')
        # else:
        #     image = Image.open('interface/pluie.png')


        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)
        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="BTC Price ₿/$", value= round( binance_df['rate_float'] ,3))
        # kpi2.metric(label="Predicted close Price", value= binance_df['rate_float'] )
        kpi2.image(image)
        kpi3.metric(label="Predicted close Price", value= round( pred_df.iloc[-1:]['Predicted Close'], 3) )
        
        time.sleep(50)
    #placeholder.empty()