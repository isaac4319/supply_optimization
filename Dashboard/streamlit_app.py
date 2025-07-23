import streamlit as st
import pandas as pd
import joblib

df = pd.read_csv("../data/forecasted_demand.csv")
sku = st.selectbox("Choose SKU", df['sku'].unique())
wh = st.selectbox("Choose Warehouse", df['warehouse'].unique())
df2 = pd.read_csv("../Data/data/demand.csv")

df2['date'] = pd.to_datetime(df2['date'])

st.title("Intelligent Demand Forecast")

st.write("Enter a product and warehouse, and get tomorrow’s forecast based on recent behavior.")

#User inputs
sku_input = st.text_input("SKU ID", value="P1079")
warehouse_input = st.text_input("warehouse", value="W01")
today_input = st.date_input("Today's Date", pd.Timestamp.today().date())

#Forecast trigger
if st.button("Forecast Tomorrow's Demand"):

    # --- Prepare data ---
    today = pd.to_datetime(today_input)
    yesterday = today - pd.Timedelta(days=1)
    last_7_days = pd.date_range(end=yesterday, periods=7)
    model = joblib.load("../Notebooks/ML_model.ipynb")

    #Filter for that SKU & warehouse
    filtered = df2[
        (df2['sku'] == sku_input) &
        (df2['warehouse'] == warehouse_input)
    ].sort_values("date")

    #Extract lag_1 and rolling_7
    try:
        lag_1 = filtered.loc[filtered['date'] == yesterday, 'demand_units'].values[0]
        rolling_7 = filtered[filtered['date'].isin(last_7_days)]['demand_units'].mean()
        day_of_week = today.dayofweek  # Assuming you're predicting for "tomorrow" based on today's weekday

        # --- Predict ---
        features = pd.DataFrame([{
            'lag_1': lag_1,
            'rolling_7': rolling_7,
            'day_of_week': day_of_week
        }])
        forecast = model.predict(features)[0]

        st.success(f"Forecasted demand for **{sku_input}** in **{warehouse_input}** on **{today + pd.Timedelta(days=1):%A, %B %d}** is **{forecast:.2f} units**.")

    except IndexError:
        st.error(" Could not compute forecast: missing demand data for yesterday.")
