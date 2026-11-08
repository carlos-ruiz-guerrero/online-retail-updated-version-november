import sqlite3

conn = sqlite3.connect(
    "retail.db"
)

rfm = pd.read_sql(
    """
    SELECT *
    FROM customer_segments
    """,
    conn
)

conn.close()
