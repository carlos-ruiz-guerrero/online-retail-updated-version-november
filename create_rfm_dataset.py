import pandas as pd

# --------------------------------------------------
# Load clean transaction dataset
# --------------------------------------------------

df = pd.read_csv("online_retail_clean.csv")

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

# --------------------------------------------------
# Build RFM table
# --------------------------------------------------

snapshot_date = (
    df["InvoiceDate"].max()
)

rfm = (
    df.groupby("CustomerID")
    .agg(
        Recency=(
            "InvoiceDate",
            lambda x:
            (snapshot_date - x.max()).days
        ),
        Frequency=(
            "InvoiceNo",
            "nunique"
        ),
        Monetary=(
            "Revenue",
            "sum"
        )
    )
    .reset_index()
)

# --------------------------------------------------
# Create segments
# --------------------------------------------------

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

# --------------------------------------------------
# Save
# --------------------------------------------------

rfm.to_csv(
    "customer_rfm.csv",
    index=False
)

print(
    f"Saved {len(rfm):,} customers"
)

print(
    "customer_rfm.csv created successfully"
)