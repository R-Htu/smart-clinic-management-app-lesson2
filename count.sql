USE students_db;

-- Create the table
CREATE TABLE staff_count_demo (
    id    INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- Insert data INCLUDING NULLs
INSERT INTO staff_count_demo (email, phone) VALUES
('alice@clinic.com', '09111111'),   -- row 1: both filled
('bob@clinic.com',   NULL),         -- row 2: phone is NULL
('carol@clinic.com', '09333333'),   -- row 3: both filled
(NULL,               '09444444');   -- row 4: email is NULL

-- View all data
SELECT * FROM staff_count_demo;

-- COUNT(*) counts ALL rows including NULLs
SELECT COUNT(*) AS count_all
FROM staff_count_demo;
-- Result: 4

-- COUNT(email) skips NULL emails
SELECT COUNT(email) AS count_email
FROM staff_count_demo;
-- Result: 3 (row 4 skipped)

-- COUNT(phone) skips NULL phones
SELECT COUNT(phone) AS count_phone
FROM staff_count_demo;
-- Result: 3 (row 2 skipped)

-- See all three together side by side
SELECT
    COUNT(*)      AS count_all_rows,
    COUNT(email)  AS count_emails,
    COUNT(phone)  AS count_phones
FROM staff_count_demo;

/*
```

## Expected Results:

### `SELECT * FROM staff_count_demo`:
```
id | email             | phone
---|-------------------|----------
1  | alice@clinic.com  | 09111111
2  | bob@clinic.com    | NULL
3  | carol@clinic.com  | 09333333
4  | NULL              | 09444444
```

### Side by side COUNT result:
```
count_all_rows | count_emails | count_phones
---------------|--------------|-------------
4              | 3            | 3 
*/