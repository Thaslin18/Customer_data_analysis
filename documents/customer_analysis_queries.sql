-- Customer Data Analysis SQL
SELECT COUNT(DISTINCT Customer_ID) AS customers,
       AVG(Total_Spend) AS average_spend, SUM(Total_Spend) AS total_spend,
       AVG(Orders) AS average_orders
FROM customer_data;

SELECT Region, COUNT(DISTINCT Customer_ID) AS customers,
       SUM(Total_Spend) AS total_spend, AVG(Total_Spend) AS average_spend
FROM customer_data GROUP BY Region ORDER BY total_spend DESC;

SELECT Loyalty_Tier, COUNT(DISTINCT Customer_ID) AS customers,
       AVG(Total_Spend) AS average_spend, SUM(Total_Spend) AS total_spend
FROM customer_data GROUP BY Loyalty_Tier ORDER BY total_spend DESC;

SELECT Online_Shopping, AVG(Orders) AS avg_orders, AVG(Total_Spend) AS avg_spend
FROM customer_data GROUP BY Online_Shopping;

SELECT Customer_ID, Total_Spend, Orders, Loyalty_Tier
FROM customer_data WHERE Total_Spend >= 20000 ORDER BY Total_Spend DESC;
