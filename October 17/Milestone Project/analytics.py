import pandas as pd
import os

# Paths
INPUT_FILE = "ETL module/processed_shipments.csv"
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Load processed shipment data
df = pd.read_csv(INPUT_FILE, parse_dates=["DispatchDate", "DeliveryDate"])

# 1. Average delivery time per warehouse
df["DeliveryDays"] = (df["DeliveryDate"] - df["DispatchDate"]).dt.days
avg_delivery = df.groupby("WarehouseID")["DeliveryDays"].mean().reset_index()
avg_delivery.rename(columns={"DeliveryDays": "AvgDeliveryDays"}, inplace=True)
avg_delivery.to_csv(f"{REPORT_DIR}/avg_delivery_time_per_warehouse.csv", index=False)

# 2. Total shipment value per product category
df["TotalValue"] = df["Quantity"] * df["UnitPrice"]
total_value = df.groupby("Category")["TotalValue"].sum().reset_index()
total_value.to_csv(f"{REPORT_DIR}/total_value_per_category.csv", index=False)

# 3. Number of shipments per month
df["Month"] = df["DispatchDate"].dt.to_period("M").astype(str)
monthly_shipments = df.groupby("Month").size().reset_index(name="ShipmentsCount")
monthly_shipments.to_csv(f"{REPORT_DIR}/shipments_per_month.csv", index=False)


# 4. Late Deliveries (DeliveryDays > 5)
late_deliveries = df[df["DeliveryDays"] > 5][
    ["ShipmentID", "ProductID", "WarehouseID", "DeliveryDays"]]
late_deliveries.to_csv(f"{REPORT_DIR}/late_deliveries.csv", index=False)

print(" Reports generated:")
print(" avg_delivery_time_per_warehouse.csv")
print(" total_value_per_category.csv")
print(" shipments_per_month.csv")
print(" late_deliveries.csv")
