import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
dbuser=os.getenv("DBUSER")
dbpw=os.getenv("DBPASSWORD")
mydb=mysql.connector.connect(
	host="localhost",
	user=dbuser,
	password=dbpw
)
mycursor = mydb.cursor()
try:
    mycursor.execute("DROP DATABASE supermarket")
except:
    pass
mycursor.execute("CREATE DATABASE supermarket")
mydb=mysql.connector.connect(
	host="localhost",
	user=dbuser,
	password=dbpw,
    db="supermarket"
)
mycursor = mydb.cursor()
mycursor.execute('CREATE TABLE products(Id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Quantity INT)')
mycursor.execute('CREATE TABLE orders(OrderId int AUTO_INCREMENT PRIMARY KEY, CustomerId int, Deliver int, Paid int, Collected int)')
mycursor.execute('CREATE TABLE orderItems(OrderId int, CustomerId int, ProductId int, Quantity int)')
print("database and fields created")
