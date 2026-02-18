USE students_db;

-- Create a sample sales table
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    salesperson VARCHAR(50),
    product VARCHAR(50),
    amount DECIMAL(10,2),
    sale_date DATE
);

-- Insert sample data
INSERT INTO sales (salesperson, product, amount, sale_date) VALUES
('Alice', 'Phone',   500.00, '2026-01-01'),
('Alice', 'Laptop', 1200.00, '2026-01-02'),
('Alice', 'Phone',   500.00, '2026-01-05'),
('Bob',   'Tablet',  300.00, '2026-01-01'),
('Bob',   'Phone',   500.00, '2026-01-03'),
('Bob',   'Laptop', 1200.00, '2026-01-04'),
('Carol', 'Tablet',  300.00, '2026-01-02'),
('Carol', 'Tablet',  300.00, '2026-01-06');

select * from sales;