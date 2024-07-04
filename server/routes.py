from app import app
from flask import request


# get entire list of products database
# GET /products
@app.route("/products", methods=["GET"])
def getProducts():
    pass

# edit fields of product database
# PUT /products?{field to edit}={new value}
@app.route("/products", methods=["PUT"])
def editProducts():
    pass



# create new order
@app.route('/orders', methods=["POST"])
def newOrder():
    pass

# confirm order is complete
@app.route('/completed/<Id>')
def confirmOrder(Id):
    pass

