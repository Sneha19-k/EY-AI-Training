from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
import uvicorn

app = FastAPI()
CSV_FILE = '../warehouses.csv'

class Warehouse(BaseModel):
    WarehouseID: str
    Location: str
    Capacity: int

def load_warehouses():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["WarehouseID", "Location", "Capacity"])

def save_warehouses(df):
    df.to_csv(CSV_FILE, index=False)

@app.get("/warehouses", response_model=List[Warehouse])
def get_warehouses():
    df = load_warehouses()
    return df.to_dict(orient="records")

@app.post("/warehouses", response_model=Warehouse)
def add_warehouse(warehouse: Warehouse):
    df = load_warehouses()
    if warehouse.WarehouseID in df["WarehouseID"].values:
        raise HTTPException(status_code=400, detail="WarehouseID already exists")
    df = pd.concat([df, pd.DataFrame([warehouse.dict()])], ignore_index=True)
    save_warehouses(df)
    return warehouse

@app.put("/warehouses/{warehouse_id}", response_model=Warehouse)
def update_warehouse(warehouse_id: str, updated: Warehouse):
    df = load_warehouses()
    if warehouse_id not in df["WarehouseID"].values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    df.loc[df["WarehouseID"] == warehouse_id, :] = list(updated.dict().values())
    save_warehouses(df)
    return updated

@app.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: str):
    df = load_warehouses()
    if warehouse_id not in df["WarehouseID"].values:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    df = df[df["WarehouseID"] != warehouse_id]
    save_warehouses(df)
    return {"message": f"Warehouse {warehouse_id} deleted"}

if __name__ == "__main__":
    uvicorn.run("warehouses_api:app", host="127.0.0.1", port=8000, reload=True)
