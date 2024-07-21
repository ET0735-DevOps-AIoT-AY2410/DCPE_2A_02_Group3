from flask import Flask
import mysql.connector
import os
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
dbuser=os.getenv("DBUSER")
dbhost=os.getenv("DBHOST")
dbpw=os.getenv("DBPASSWORD")
def getdb():
    db=mysql.connector.connect(
	host=dbhost,
	user=dbuser,
	password=dbpw,
	db="supermarket"
    )
    return db


