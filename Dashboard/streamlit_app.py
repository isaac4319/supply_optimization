import streamlit as st
import pandas as pd
st.title("Supply Chain Forecast")

df = pd.read_csv("../data/forecasted_demand.csv")
sku = st.selectbox("Choose SKU", df['sku'].unique())
wh = st.selectbox("Choose Warehouse", df['warehouse'].unique())

filtered = df[(df['sku'] == sku) & (df['warehouse'] == wh)]
filtered['date'] = pd.to_datetime(filtered['date'])
st.line_chart(filtered.set_index('date')['forecasted_demand_units'])