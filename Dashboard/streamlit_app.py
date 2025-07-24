import streamlit as st
import pandas as pd
import joblib
from pyngrok import ngrok
import os
from pyngrok import conf

conf.get_default().auth_token = os.getenv("30KG7CXJ98uCMAWO4MvYyDrYUrc_2BhKFvpHZhVFRWbG3iz7d")

public_url = ngrok.connect(port=8501)
print(f"Public URL: {public_url}")

df2 = pd.read_csv("Data/data/demand.csv")
df2['date'] = pd.to_datetime(df2['date'])

model = joblib.load("Data/lgbm_model.pkl")

st.title("Intelligent Demand Forecast")

sku_input = st.text_input("SKU ID", value="P1079")
warehouse_input = st.text_input("Warehouse", value="W01")
today_input = st.date_input("Today's Date", pd.Timestamp.today().date())

if st.button("Forecast Tomorrow's Demand"):
    today = pd.to_datetime(today_input)
    yesterday = today - pd.Timedelta(days=1)
    last_7_days = pd.date_range(end=yesterday, periods=7)

    filtered = (
        df2[(df2['sku'] == sku_input) & (df2['warehouse'] == warehouse_input)]
        .sort_values("date")
    )

    if filtered.empty:
        st.error(f"No historical demand data for SKU {sku_input} at warehouse {warehouse_input}.")
        st.stop()

    lag_data = filtered.loc[filtered['date'] == yesterday, 'demand_units']
    if not lag_data.empty:
        lag_1 = lag_data.values[0]
    else:
        lag_1 = filtered['demand_units'].iloc[-1]

    window = filtered[filtered['date'].isin(last_7_days)]['demand_units']
    if not window.empty:
        rolling_7 = window.mean()
    else:
        rolling_series = filtered['demand_units'].rolling(7).mean().dropna()
        if not rolling_series.empty:
            rolling_7 = rolling_series.iloc[-1]
        else:
            rolling_7 = filtered['demand_units'].mean()

    day_of_week = today.dayofweek

    features = pd.DataFrame([{
        'lag_1': lag_1,
        'rolling_7': rolling_7,
        'day_of_week': day_of_week
    }])
    forecast = model.predict(features)[0]

    forecast_date = (today + pd.Timedelta(days=1)).strftime("%A, %B %d")
    st.success(
        f"Forecasted demand for {sku_input} in {warehouse_input} on {forecast_date}: "
        f"{forecast:.2f} units."
    )
