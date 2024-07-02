CREATE DATABASE supermarket;
use supermarket;
CREATE TABLE products(Id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Quantity INT);
CREATE TABLE orders(OrderId int AUTO_INCREMENT PRIMARY KEY, Deliver int, Paid int, Collected int);
CREATE TABLE orderItems(OrderId int, ProductId int, Quantity int);
