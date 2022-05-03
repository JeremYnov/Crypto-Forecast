from matplotlib.pyplot import title
import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
import time
from datetime import date
from PIL import Image

st.set_page_config(layout="wide")

today = date.today()

# creating a single-element container.
placeholder = st.empty()

# Request API URL 
response = requests.get("http://app:5000/btcPrice").json()
df = pd.DataFrame(response)
df = df.set_index('Date')

pred_response = requests.get("http://app:5000/predPrice").json()
pred_df = pd.DataFrame(pred_response)
pred_df = pred_df.set_index('Date')

comparison_df = df.join(pred_df)
comparison_df = comparison_df.drop(['High','Low','Open','Volume','Predicted High','Predicted Low','Predicted Open','Predicted Volume'], axis=1)
comparison_df = comparison_df.dropna()


# Create candlestick chart for bitcoin
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))

# Create candlestick chart for bitcoin predictions
pred_fig = go.Figure()
pred_fig.add_trace(go.Candlestick(x=pred_df.index, open=pred_df['Predicted Open'], high=pred_df['Predicted High'], low=pred_df['Predicted Low'], close=pred_df['Predicted Close']))
# create three columns
col1, col2 = st.columns(2)
with col1:
    st.header("          Bitcoin prices")
    st.plotly_chart(fig)

with col2:
    st.header("          Bictoin prediction prices")
    st.plotly_chart(pred_fig)

new_fig = go.Figure()
new_fig.add_trace(go.Scatter(
    x=comparison_df.index,
    y=comparison_df['Close'],
    marker=dict(
        color="blue"
    ),
    showlegend=False
))

new_fig.add_trace(go.Scatter(
    x=comparison_df.index,
    y=comparison_df['Predicted Close'],
    marker=dict(
        color="red"
    ),
    showlegend=False
))
   
col3, col4 = st.columns(2)
with col3:
    st.dataframe(comparison_df)
    

with col4:
    st.plotly_chart(new_fig)
    
sa_response = requests.get("http://app:5000/sentiment").json()
sa_df = pd.DataFrame(sa_response)

st.dataframe(sa_df)


while True: 
    with placeholder.container():
        
        coindesk_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        coindesk_response = requests.get(coindesk_url).json()
        coindesk_df = pd.DataFrame(coindesk_response['bpi']['USD'], index=[0])
        
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)
        
        
        if coindesk_df['rate_float'].values[0] < pred_df.iloc[-1:]['Predicted Close'].values[0]:
            image = Image.open('soleil.png')
        else: 
            image = Image.open('pluie.png')

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="BTC Price ₿/＄", value= round( coindesk_df['rate_float'] ,3))
        # kpi2.metric(label="Predicted close Price", value= binance_df['rate_float'] )
        kpi2.image(image)
        kpi3.metric(label="Predicted close Price", value= round( pred_df.iloc[-1:]['Predicted Close'].values[0], 3) )
        
        time.sleep(50)
    #placeholder.empty()