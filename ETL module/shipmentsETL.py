import pandas as pd

# Extract - Read CSV files
products = pd.read_csv("../products.csv")
warehouses = pd.read_csv("../warehouses.csv")
shipments = pd.read_csv("shipments.csv", parse_dates=["DispatchDate", "DeliveryDate"])

# Transform - Join and calculate columns
df = shipments.merge(products, on="ProductID", how="left")
df = df.merge(warehouses, on="WarehouseID", how="left")

#Adding new column
df["TotalValue"] = df["Quantity"] * df["UnitPrice"]
df["DeliveryDays"] = (df["DeliveryDate"] - df["DispatchDate"]).dt.days

# Load - Save the processed data
df.to_csv("processed_shipments.csv", index=False)
print("ETL Pipeline Completed. Processed data saved to processed_shipments.csv")
