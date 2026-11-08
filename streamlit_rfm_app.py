import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("customer_rfm.csv")

rfm = load_data()

# ============================================================
# HEADER
# ============================================================

st.title("🛍️ Customer Segmentation Dashboard")

st.markdown("""
This dashboard analyzes customer purchasing behaviour using
RFM (Recency, Frequency, Monetary) metrics.

The objective is to identify customer segments and generate
actionable business insights that support marketing,
customer retention, and sales optimization.
""")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Filters")

segments = st.sidebar.multiselect(
    "Select Customer Segments",
    options=sorted(rfm["Segment"].unique()),
    default=sorted(rfm["Segment"].unique())
)

filtered = rfm[
    rfm["Segment"].isin(segments)
]

# ============================================================
# KPIs
# ============================================================

st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{len(filtered):,}"
)

col2.metric(
    "Avg Recency",
    f"{filtered['Recency'].mean():.0f} days"
)

col3.metric(
    "Avg Frequency",
    f"{filtered['Frequency'].mean():.1f}"
)

col4.metric(
    "Avg Monetary",
    f"£{filtered['Monetary'].mean():,.0f}"
)

# ============================================================
# SEGMENT DISTRIBUTION
# ============================================================

st.markdown("---")
st.subheader("🎯 Customer Segment Distribution")

segment_counts = (
    filtered["Segment"]
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
    values="Count",
    hole=0.4
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
    filtered,
    x="Frequency",
    y="Monetary",
    color="Segment",
    size="Monetary",
    hover_data=[
        "CustomerID",
        "Recency"
    ],
    title="Frequency vs Monetary Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# RECENCY DISTRIBUTION
# ============================================================

st.markdown("---")
st.subheader("⏳ Customer Recency Distribution")

fig = px.histogram(
    filtered,
    x="Recency",
    color="Segment",
    nbins=40,
    title="Customer Activity Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEGMENT PROFILE
# ============================================================

st.markdown("---")
st.subheader("📈 Segment Profiles")

segment_profile = (
    filtered
    .groupby("Segment")
    .agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    })
    .round(2)
    .reset_index()
)

fig = px.bar(
    segment_profile,
    x="Segment",
    y="Monetary",
    color="Segment",
    title="Average Monetary Value by Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SEGMENT COMPARISON TABLE
# ============================================================

st.markdown("---")
st.subheader("📋 Segment Comparison")

st.dataframe(
    segment_profile,
    use_container_width=True
)

# ============================================================
# TOP CUSTOMERS
# ============================================================

st.markdown("---")
st.subheader("🏆 Top Customers")

top_customers = (
    filtered
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_customers,
    use_container_width=True
)

# ============================================================
# DOWNLOAD DATA
# ============================================================

st.markdown("---")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=filtered.to_csv(index=False),
    file_name="customer_rfm_filtered.csv",
    mime="text/csv"
)

# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("---")
st.subheader("💡 Business Insights")

largest_segment = (
    filtered["Segment"]
    .value_counts()
    .idxmax()
)

highest_value_segment = (
    filtered.groupby("Segment")
    ["Monetary"]
    .mean()
    .idxmax()
)

st.info(
    f"""
    • Largest segment: {largest_segment}

    • Highest average value segment: {highest_value_segment}

    • Customers in the highest-value segment should be prioritised
      for retention and loyalty initiatives.

    • Lower-value segments may benefit from targeted promotional
      campaigns and engagement strategies.
    """
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    """
    Customer Segmentation Dashboard
    Built with Python, Pandas, Plotly and Streamlit
    """
)