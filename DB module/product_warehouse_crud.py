import pandas as pd

products = pd.read_csv('../products.csv')
warehouses = pd.read_csv('../warehouses.csv')

# Add new product
new_product = pd.DataFrame([{
    'ProductID': 'P106',
    'ProductName': 'Webcam',
    'Category': 'Accessories',
    'UnitPrice': 50
}])
products = pd.concat([products, new_product], ignore_index=True)

# Update warehouse capacity
warehouses.loc[warehouses['WarehouseID'] == 'W01', 'Capacity'] = 1200

# Delete product
products = products[products['ProductID'] != 'P102']

# Fetch all Electronics products
electronics = products[products['Category'] == 'Electronics']
print(electronics)
