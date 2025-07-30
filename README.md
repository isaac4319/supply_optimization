Optimizing a fragmented supply chain using Machine Learning and Big Data techniques

This project was made to provide a solution to an ever growing problem in global supply chains. Companies are currently often experiencing slowdowns in various parts of supply chains which quickly propagates down the chain, severely affecting company performance.

Given this, it has become critical for companies to be able to have foresight on their supply chains and be able to adjust in real time to incoming data. Therefore in this project I have created a hybrid optimization and forecasting model which allows a hypothetical operator of a supply chain to be able to see the projected demand for the following day from each warehouse.

The problem context:
This is a notional simulation that provides simulated inbound data that an operator may receive from its warehouse network. These are:
- Demand data for SKU's or Stock Keeping Units(Unique identifiers for individual products)
- Inventory data that defines the current stock level of SKU's in each warehouse
- Transport cost data which defines the cost of transporting each unit between warehouse with all warehouse combinations

Solution created:

A predictive model based on LightGBM (LGBMRegressor) forecasts next-day SKU demand. I have chosen an LGBM as it handles noisy data very well which is common in supply chains, errors will be made when sending data or recording it.
Optimization Engine:
-An optimization module redistributes stock across warehouses to match predicted demand, while minimizing transportation costs.
Interactive Application:
The full pipeline is deployed via a Streamlit app, allowing supply chain operators to:
-Visualize forecasted demand trends
-Input real-time data
-Optimize inventory allocations with a single click