import pandas as pd
from datetime import datetime
import os

# Extract - Read CSV files
products = pd.read_csv("../products.csv")
warehouses = pd.read_csv("../warehouses.csv")
shipments = pd.read_csv("shipments.csv", parse_dates=["DispatchDate", "DeliveryDate"])

# Transform - Join and calculate columns
df = shipments.merge(products, on="ProductID", how="left")
df = df.merge(warehouses, on="WarehouseID", how="left")

# Add calculated columns
df["TotalValue"] = df["Quantity"] * df["UnitPrice"]
df["DeliveryDays"] = (df["DeliveryDate"] - df["DispatchDate"]).dt.days

# Load - Save the processed data with dynamic filename
today = datetime.now().strftime("%Y%m%d")
output_dir = "daily_reports"
os.makedirs(output_dir, exist_ok=True)

output_file = f"{output_dir}/daily_shipments_{today}.csv"
df.to_csv(output_file, index=False)

print(f"✅ ETL Pipeline Completed. Processed data saved to {output_file}")
