import uvicorn
from fastapi import FastAPI,APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

app = FastAPI()

router = APIRouter()
CSV_FILE = '../products.csv'

class Product(BaseModel):
    ProductID: str
    ProductName: str
    Category: str
    UnitPrice: float

def load_products() -> pd.DataFrame:
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["ProductID", "ProductName", "Category", "UnitPrice"])

def save_products(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

# GET all products
@router.get("/products", response_model=List[Product])
def get_products():
    df = load_products()
    return df.to_dict(orient="records")

# POST add new product
@router.post("/products", response_model=Product)
def add_product(product: Product):
    df = load_products()
    if product.ProductID in df["ProductID"].values:
        raise HTTPException(status_code=400, detail="ProductID already exists")
    # Append new product
    df = pd.concat([df, pd.DataFrame([product.dict()])], ignore_index=True)
    save_products(df)
    return product

# PUT update product details
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, updated_product: Product):
    df = load_products()
    if product_id not in df["ProductID"].values:
        raise HTTPException(status_code=404, detail="Product not found")
    # Update the row
    df.loc[df["ProductID"] == product_id, :] = list(updated_product.dict().values())
    save_products(df)
    return updated_product

# DELETE a product
@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    df = load_products()
    if product_id not in df["ProductID"].values:
        raise HTTPException(status_code=404, detail="Product not found")
    df = df[df["ProductID"] != product_id]
    save_products(df)
    return {"message": f"Product {product_id} deleted"}


app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("product_api:app", host="127.0.0.1", port=8000, reload=True)