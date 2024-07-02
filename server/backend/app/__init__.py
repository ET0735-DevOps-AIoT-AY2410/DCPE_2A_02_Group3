from flask import Flask
import mysql.connector
import os
app=Flask(__name__)
def getdb():
    db=mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="supermarket"
    )
    return db


