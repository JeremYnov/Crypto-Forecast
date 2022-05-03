import streamlit as st

from multiapp import MultiApp
from apps import bitcoin


app = MultiApp()

st.markdown(
    """
    # Crypto-Forecaste
    """
)

# Every app is a page on interface
app.add_app("Bitcoin Dashboard", bitcoin.app)

# Run the app
app.run()