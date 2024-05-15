import streamlit as st
import pandas as pd

@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df
