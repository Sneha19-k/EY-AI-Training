import pandas as pd
from datetime import datetime

def run_pipeline():
    df= pd.read_csv("inventory.csv")

    def restock_need(row):
        if row["Quantity"] < row["ReorderLevel"]:
            return "Yes"
        else:
            return "No"

    df["RestockNeeded"] = df.apply(restock_need, axis=1)
    df["TotalValue"] = df["Quantity"] * df["PricePerUnit"]

    df.to_csv("restock_report.csv", index=False)
    print(f"Inventory pipeline completed at {datetime.now()}")

if __name__ == "__main__":
    run_pipeline()