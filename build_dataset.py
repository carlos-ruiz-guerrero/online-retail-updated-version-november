from ucimlrepo import fetch_ucirepo
import pandas as pd

print("Downloading dataset...")

online_retail = fetch_ucirepo(id=352)

df = online_retail.data.original.copy()

print(f"Raw records: {len(df):,}")

# -------------------------------------------------
# Cleaning
# -------------------------------------------------

df = df.dropna(subset=["CustomerID"])

df = df[df["Quantity"] > 0]

df = df[df["UnitPrice"] > 0]

df = df[
    ~df["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

df = df.drop_duplicates()

# -------------------------------------------------
# Date conversion
# -------------------------------------------------

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

# -------------------------------------------------
# Revenue
# -------------------------------------------------

df["Revenue"] = (
    df["Quantity"]
    * df["UnitPrice"]
)

# -------------------------------------------------
# Save
# -------------------------------------------------

df.to_csv(
    "online_retail_clean.csv",
    index=False
)

print(
    f"Clean records: {len(df):,}"
)

print(
    "Saved: online_retail_clean.csv"
)