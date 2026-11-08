import sqlite3
import pandas as pd

print("Loading dataset...")

df = pd.read_csv(
    "online_retail_clean.csv"
)

print(f"Records: {len(df):,}")

conn = sqlite3.connect("retail.db")

df.to_sql(
    "transactions",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

print("Database created successfully.")
print("Table: transactions")