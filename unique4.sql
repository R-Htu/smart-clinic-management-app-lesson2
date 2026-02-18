USE students_db;
-- Step 6: Delete duplicates (keeps the row with LOWEST staff_id)

DELETE s1 FROM staff_test s1
INNER JOIN staff_test s2
WHERE s1.staff_id > s2.staff_id
AND s1.email = s2.email;

-- Step 7: Verify duplicates are gone
SELECT * FROM staff_test;