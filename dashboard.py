import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st
import iaea_access

st.set_page_config(
    page_title="IAEA Nuclear Database API frontend",
    page_icon="☢️",
    layout="wide",
)

st.title("I want to import some nuclear data")
Data to look = st.selectbox("Select the Job", ('Ground States',))
