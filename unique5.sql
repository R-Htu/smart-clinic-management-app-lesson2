use students_db;
ALTER TABLE staff_test
ADD CONSTRAINT unique_email UNIQUE (email);

-- Step 9: Test - try inserting duplicate again (this will FAIL now)
INSERT INTO staff_test (email, full_name)
VALUES ('nandar@clinic.com', 'Try Duplicate');

-- Step 10: View final clean data
SELECT * FROM staff_test;