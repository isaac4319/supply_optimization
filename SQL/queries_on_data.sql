-- Demand table
CREATE OR REPLACE TABLE demand (
    sku STRING,
    warehouse STRING,
    date DATE,
    demand_units INT
);

-- Inventory table
CREATE OR REPLACE TABLE inventory (
    sku STRING,
    warehouse STRING,
    date DATE,
    stock_level INT
);

-- Transport cost table
CREATE OR REPLACE TABLE transport_costs (
    from_warehouse STRING,
    to_warehouse STRING,
    cost_per_unit FLOAT
);

-- Monthly demand summary
CREATE OR REPLACE VIEW monthly_demand AS
SELECT 
    sku,
    warehouse,
    DATE_TRUNC('month', date) AS month,
    SUM(demand_units) AS monthly_demand
FROM demand
GROUP BY sku, warehouse, month;
