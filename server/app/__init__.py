from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
db=mysql.connector.connect(
	host="localhost",
	user=os.getenv("DBUSER"),
	password=os.getenv("DBPASSWORD")
    database="supermarket"
)
DB=db.cursor()


