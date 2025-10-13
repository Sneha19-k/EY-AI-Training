import pandas as pd
from datetime import datetime

def run_pipeline():
    df1= pd.read_csv("customers.csv")
    df2= pd.read_csv("orders.csv")
    df3= pd.read_csv("products.csv")

    # Join orders with customers on CustomerID
    orders_customers = pd.merge(df2, df1, on="CustomerID", how="left")

    # Join the result with products on ProductID
    full_data = pd.merge(orders_customers, df3, on="ProductID", how="left")

    # add col TotalAmount
    full_data["TotalAmount"] = full_data["Quantity"] * full_data["Price"]

    # Convert OrderDate to datetime and extract month
    full_data["OrderDate"] = pd.to_datetime(full_data["OrderDate"])
    full_data["OrderMonth"] = full_data["OrderDate"].dt.to_period("M").astype(str)

    # filter data
    filtered_data = full_data[
        (full_data["Quantity"] >= 2) &
        (full_data["Country"].isin(["India", "UAE"]))
        ]

    #group and aggregate

    revenue_by_category = (
        filtered_data.groupby("Category")["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    revenue_by_segment = (
        filtered_data.groupby("Segment")["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    # sort customers

    customer_revenue = (
        filtered_data.groupby(["CustomerID", "Name"])["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
        .sort_values(by="TotalRevenue", ascending=False)
    )

    # Load

    filtered_data.to_csv("processed_orders.csv", index=False)
    revenue_by_category.to_csv("category_summary.csv", index=False)
    revenue_by_segment.to_csv("segment_summary.csv", index=False)
    customer_revenue.to_csv("customer_revenue_ranking.csv", index=False)

    print(f"Sales pipeline completed at {datetime.now()}")

if __name__ == "__main__":
    run_pipeline()



