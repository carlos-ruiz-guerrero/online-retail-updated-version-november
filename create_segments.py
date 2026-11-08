import sqlite3
import pandas as pd

conn = sqlite3.connect("retail.db")

rfm = pd.read_sql(
    "SELECT * FROM customer_rfm",
    conn
)

rfm["Segment"] = pd.qcut(
    rfm["Monetary"],
    q=4,
    labels=[
        "Low Value",
        "Medium",
        "High",
        "VIP"
    ],
    duplicates="drop"
)

rfm.to_sql(
    "customer_segments",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print(
    "customer_segments table created."
)