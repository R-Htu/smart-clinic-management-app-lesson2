USE students_db;

SELECT salesperson, SUM(amount) AS total_earned
FROM sales
GROUP BY salesperson;

