USE students_db;

ALTER TABLE staff_test
ADD CONSTRAINT unique_email UNIQUE (email);

SELECT * from staff_test;
