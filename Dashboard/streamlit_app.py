import streamlit as st
import pandas as pd
import joblib

# Load historical demand data
df2 = pd.read_csv("../Data/data/demand.csv")
df2['date'] = pd.to_datetime(df2['date'])

# Load the trained model
model = joblib.load("../Data/lgbm_model.pkl")

st.title("Intelligent Demand Forecast")

# User inputs
sku_input = st.text_input("SKU ID", value="P1079")
warehouse_input = st.text_input("Warehouse", value="W01")
today_input = st.date_input("Today's Date", pd.Timestamp.today().date())

if st.button("Forecast Tomorrow's Demand"):
    # Prepare dates
    today = pd.to_datetime(today_input)
    yesterday = today - pd.Timedelta(days=1)
    last_7_days = pd.date_range(end=yesterday, periods=7)

    # Filter history for this SKU and warehouse
    filtered = (
        df2[(df2['sku'] == sku_input) & (df2['warehouse'] == warehouse_input)]
        .sort_values("date")
    )

    # Compute lag_1 (yesterday) with fallback
    try:
        lag_1 = filtered.loc[filtered['date'] == yesterday, 'demand_units'].values[0]
    except IndexError:
        lag_1 = filtered['demand_units'].iloc[-1]

    # Compute 7‑day rolling average with fallback
    window = filtered[filtered['date'].isin(last_7_days)]['demand_units']
    if not window.empty:
        rolling_7 = window.mean()
    else:
        rolling_7 = filtered['demand_units'].rolling(7).mean().iloc[-1]

    day_of_week = today.dayofweek

    # Build feature vector and predict
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
