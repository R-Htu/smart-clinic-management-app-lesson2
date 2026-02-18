-- Without GROUP BY (shows every single row)
use students_db;


-- With GROUP BY (groups them together and counts)
SELECT salesperson, COUNT(*) AS total_sales
FROM sales
GROUP BY salesperson;
/*

**Result:**

salesperson | total_sales
------------|------------
Alice       | 3
Bob         | 3
Carol       | 2

```

*/