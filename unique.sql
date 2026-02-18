USE students_db;

-- Step 1: Create table WITHOUT unique (so duplicates can enter)
CREATE TABLE staff_test (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100),
    full_name VARCHAR(100)
);

-- Step 2: Insert data INCLUDING duplicates
INSERT INTO staff_test (email, full_name) VALUES
('nandar@clinic.com',  'Nandar Kyaw'),
('thandar@clinic.com', 'Thandar Hlaing'),
('aungmin@clinic.com', 'Aung Min');


-- Step 3: View all data (you will see duplicates)
SELECT * FROM staff_test;


