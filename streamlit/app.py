from matplotlib.pyplot import title
import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
import numpy as np
import plotly.express as px # interactive charts 
from datetime import date
from PIL import Image

today = date.today()

# creating a single-element container.
placeholder = st.empty()

# Request API URL 
response = requests.get("http://localhost:5000/btcPrice").json()
df = pd.DataFrame(response)

# Create candlestick chart 
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
#Display chart
st.header("Bitcoin prices from day 1")
st.plotly_chart(fig)

# TODO (change request url) Request API URL 
pred_response = requests.get("http://localhost:5000/btcPrice").json()
pred_df = pd.DataFrame(pred_response)
print(pred_df.iloc[-1:]['Close'])

while True: 

    with placeholder.container():
        binance_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        binance_response = requests.get(binance_url).json()
        binance_df = pd.DataFrame(binance_response['bpi']['USD'], index=[0])
        
        
        
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)
        
        image = Image.open('streamlit/pluie.png')

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="BTC Price ₿/＄", value= round( binance_df['rate_float'] ,3))
        # kpi2.metric(label="Predicted close Price", value= binance_df['rate_float'] )
        kpi2.image(image)
        kpi3.metric(label="Predicted close Price", value= round( pred_df.iloc[-1:]['Close'], 3) )
        
        # kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
        # kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)
        time.sleep(50)
    #placeholder.empty()