import redis
import json
import time
import pandas as pd
import os
import logging

CSV_FILE = "../ETL module/processed_shipments.csv"

# Configure logging to save to app.log
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load or create shipments DataFrame, ensure Status is read as string to reduce issues
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE, dtype={"Status": str})
else:
    df = pd.DataFrame(columns=["ShipmentID", "ProductID", "WarehouseID", "Status"])

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

print("Consumer started. Waiting for messages...")

while True:
    msg = r.rpop("shipment_updates")

    if msg:
        update = json.loads(msg)
        shipment_id = update.get("ShipmentID")
        product_id = update.get("ProductID")
        warehouse_id = update.get("WarehouseID")
        status = update.get("Status", "Unknown")

        # Check for missing required fields
        if not product_id or not warehouse_id:
            logging.error(f"Missing ProductID or WarehouseID in update: {update}")
            print(f"Error: Missing ProductID or WarehouseID in update: {update}")
            continue

        logging.info(f"Processing shipment {shipment_id} with status {status}")

        idx = df.index[df["ShipmentID"] == shipment_id]

        if len(idx) == 0:
            # Add new shipment record
            df.loc[len(df)] = [shipment_id, product_id, warehouse_id, status]
        else:
            # Update existing shipment status
            df.at[idx[0], "Status"] = status

        # Safely convert status to string before calling .lower()
        status_str = str(status).lower()

        # Log special events
        if status_str == "dispatched":
            logging.info(f"Shipment {shipment_id} dispatched from warehouse {warehouse_id}")
        elif status_str == "delivered":
            logging.info(f"Shipment {shipment_id} delivered successfully")

        # Save updated CSV
        df.to_csv(CSV_FILE, index=False)
        print(f"Updated CSV saved with status: {status}")

        time.sleep(1)

    else:
        # No message found, wait before retrying
        time.sleep(1)
