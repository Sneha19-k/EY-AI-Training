import redis
import json
import time
import pandas as pd

r = redis.Redis(host='localhost', port=6379, db=0)

# Path to your shipments CSV with columns ShipmentID,ProductID,WarehouseID,Status (Status column added or existing)
csv_file = "../ETL module/processed_shipments.csv"

# Read CSV file
df = pd.read_csv(csv_file)

# Iterate over rows and push to Redis
for _, row in df.iterrows():
    # Convert row to dictionary
    update = {
        "ShipmentID": row["ShipmentID"],
        "ProductID": row["ProductID"],
        "WarehouseID": row["WarehouseID"],
        "Status": row["Status"]
    }
    r.lpush("shipment_updates", json.dumps(update))
    print("Produced:", update)
    time.sleep(1)
