import sqlite3

conn = sqlite3.connect("retail.db")

cursor = conn.cursor()

# remove previous version if it exists

cursor.execute("""
DROP TABLE IF EXISTS customer_rfm;
""")

# build analytical table

cursor.execute("""
CREATE TABLE customer_rfm AS

WITH snapshot AS (

    SELECT
        MAX(InvoiceDate) AS max_date
    FROM transactions

)

SELECT

    CustomerID,

    CAST(
        julianday(
            (SELECT max_date FROM snapshot)
        )
        -
        julianday(
            MAX(InvoiceDate)
        )
        AS INTEGER
    ) AS Recency,

    COUNT(
        DISTINCT InvoiceNo
    ) AS Frequency,

    ROUND(
        SUM(Revenue),
        2
    ) AS Monetary

FROM transactions

GROUP BY CustomerID;
""")

conn.commit()

cursor.execute("""
SELECT COUNT(*)
FROM customer_rfm
""")

count = cursor.fetchone()[0]

print(
    f"Customer records: {count:,}"
)

conn.close()