import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql

# Load CSV
df = pd.read_csv(r'C:\Users\kalpe\Downloads\archive (3)\zomato_dataset.csv')

# Preview
print(df.head())

# Check NULL values
print(df.isnull().sum())

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# OPTIONAL: Remove duplicates
df.drop_duplicates(inplace=True)

# OPTIONAL: Clean Unicode characters
for col in df.select_dtypes(include='object').columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("’", "'", regex=False)
        .str.replace("–", "-", regex=False)
        .str.encode("utf-8", errors="ignore")
        .str.decode("utf-8")
    )

# MySQL Connection
engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/zomato_db?charset=utf8mb4"
)

print("✅ Connection Successful")

# Upload DataFrame to MySQL
df.to_sql(
    name='orders',
    con=engine,
    if_exists='replace',   # replace existing table
    index=False,
    chunksize=1000         # upload in batches
)

print("✅ Data Uploaded Successfully")