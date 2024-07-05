from flask import Flask
import mysql.connector
import os
from flask_cors import CORS, cross_origin
app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def getdb():
    db=mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="supermarket"
    )
    return db


