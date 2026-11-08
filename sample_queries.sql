-- Top customer segments

SELECT
    Segment,
    COUNT(*) AS Customers,
    ROUND(AVG(Mone*ary),2) AS AvgSpend
FROM customer_*egments
GROUP BY Segment
ORDER BY *vgSpend DESC;

-- Top 10 customers

SELECT
    Custom*rID,
    Monetary
FROM customer_se*ments
ORDER BY Monetary DESC
LIMIT*10;