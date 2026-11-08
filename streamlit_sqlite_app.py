import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

@st.cache_data
def load_data():

    db_path = Path(__file__).parent / "retail.db"

    conn = sqlite3.connect(db_path)

    rfm = pd.read_sql(
        """
        SELECT
            CustomerID,
            Recency,
            Frequency,
            Monetary,
            Segment
        FROM customer_segments
        ORDER BY Monetary DESC
        """,
        conn
    )

    conn.close()

    return rfm

rfm = load_data()

st.sidebar.markdown("### Data Source")

st.sidebar.info(
    f"{len(rfm):,} customers loaded"
)

st.sidebar.success(
    f"{len(rfm):,} customers loaded from SQLite"
)
