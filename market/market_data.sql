CREATE DATABASE IF NOT EXISTS market_data;
USE market_data;

-- Migros ürünleri tablosunu oluşturma
CREATE TABLE IF NOT EXISTS migros_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    image LONGBLOB
);

-- A101 ürünleri tablosunu oluşturma
CREATE TABLE IF NOT EXISTS a101_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    image LONGBLOB
);

-- Şok ürünleri tablosunu oluşturma
CREATE TABLE IF NOT EXISTS sok_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    image LONGBLOB
);

