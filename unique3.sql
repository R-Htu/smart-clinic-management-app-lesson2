USE students_db;

SELECT email, COUNT(*) AS total
FROM staff_test
GROUP BY email
HAVING COUNT(*) > 1;
