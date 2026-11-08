import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Online Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("online_retail_clean.csv")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    if "Revenue" not in df.columns:
        df["Revenue"] = (
            df["Quantity"] * df["UnitPrice"]
        )

    return df


df = load_data()

# ============================================================
# HEADER
# ============================================================

st.title("🛍️ Online Retail Customer Segmentation Dashboard")

st.markdown("""
This dashboard explores customer purchasing behaviour using the
UCI Online Retail Dataset.

### Features
- Sales Performance Analysis
- Country Revenue Analysis
- Product Performance
- RFM Customer Segmentation
- Pareto Analysis
""")

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df["Country"].dropna().unique()),
    default=sorted(df["Country"].dropna().unique())
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        df["InvoiceDate"].min().date(),
        df["InvoiceDate"].max().date()
    )
)

# ============================================================
# FILTER DATA
# ============================================================

filtered = df.copy()

filtered = filtered[
    filtered["Country"].isin(countries)
]

if isinstance(date_range, tuple):
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = pd.to_datetime(date_range)
    end_date = pd.to_datetime(date_range)

filtered = filtered[
    (filtered["InvoiceDate"] >= start_date)
    &
    (filtered["InvoiceDate"] <= end_date)
]

if filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ============================================================
# KPI SECTION
# ============================================================

total_revenue = filtered["Revenue"].sum()
total_orders = filtered["InvoiceNo"].nunique()
total_customers = filtered["CustomerID"].nunique()

avg_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"£{total_revenue:,.0f}"
)

col2.metric(
    "Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Avg Order Value",
    f"£{avg_order_value:,.2f}"
)

# ============================================================
# MONTHLY REVENUE
# ============================================================

st.markdown("---")
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered
    .set_index("InvoiceDate")
    .resample("ME")
    ["Revenue"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_revenue,
    x="InvoiceDate",
    y="Revenue",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# COUNTRY ANALYSIS
# ============================================================

st.markdown("---")
st.subheader("🌍 Revenue by Country")

country_sales = (
    filtered
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    country_sales,
    x="Revenue",
    y="Country",
    orientation="h",
    color="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# PRODUCT ANALYSIS
# ============================================================

st.markdown("---")
st.subheader("🏆 Top Products by Revenue")

top_products = (
    filtered
    .groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# RFM ANALYSIS
# ============================================================

st.markdown("---")
st.subheader("🤖 Customer Segmentation")

rfm = filtered.groupby("CustomerID").agg(
    Recency=(
        "InvoiceDate",
        lambda x: (
            filtered["InvoiceDate"].max() - x.max()
        ).days
    ),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

try:
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
except Exception:
    rfm["Segment"] = "Customer"

segment_counts = (
    rfm["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Count"
]

fig = px.pie(
    segment_counts,
    names="Segment",
    values="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CUSTOMER VALUE MATRIX
# ============================================================

st.markdown("---")
st.subheader("📊 Customer Value Matrix")

fig = px.scatter(
    rfm,
    x="Frequency",
    y="Monetary",
    color="Segment",
    size="Monetary",
    hover_data=["Recency"]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# PARETO ANALYSIS
# ============================================================

st.markdown("---")
st.subheader("💰 Pareto Analysis")

customer_sales = (
    filtered
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

cumulative = (
    customer_sales.cumsum()
    / customer_sales.sum()
) * 100

customer_pct = (
    np.arange(1, len(customer_sales) + 1)
    / len(customer_sales)
) * 100

pareto = pd.DataFrame({
    "Customers (%)": customer_pct,
    "Revenue (%)": cumulative.values
})

fig = px.line(
    pareto,
    x="Customers (%)",
    y="Revenue (%)"
)

fig.add_hline(
    y=80,
    line_dash="dash"
)

fig.add_vline(
    x=20,
    line_dash="dash"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# DATA PREVIEW
# ============================================================

st.markdown("---")
st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered.head(100),
    use_container_width=True
)

# ============================================================
# DOWNLOAD DATA
# ============================================================

st.download_button(
    label="⬇️ Download Dataset",
    data=filtered.to_csv(index=False),
    file_name="online_retail_filtered.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Built with Streamlit, Pandas and Plotly"
)