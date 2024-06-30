from app import app
from app import getdb
from flask import jsonify,request


# get entire list of products database
# GET /products
@app.route("/products", methods=["GET"])
def getProducts():
    conn=getdb()
    cur=conn.cursor()
    cur.execute("SELECT * FROM products")
    results=cur.fetchall()
    jsons=[]
    for i in results:
        jsons.append(
                {
                    "id":i[0],
                    "name":i[1],
                    "quantity":i[2]
                    })
    cur.close()
    conn.close()
    return jsons

# edit fields of product database
# requires at least id
# PUT /products?{field to edit}={new value}
@app.route("/products", methods=["PUT"])
def editProducts():
    conn=getdb()
    cur=conn.cursor()
    if request.args.get("id")==None:
        return "please specify id", "400"
    Id=request.args.get('id')
    name=request.args.get("Name")
    amt=request.args.get("Quantity")
    name=("Name = "+name+' ') if not name == None else ""
    amt=("Quantity = "+amt) if not amt == None else ""
    if (name =='' and amt ==''):
        return "Please include changes",400
    if (name !='' and amt !=''):
        name+=", "
    print(f'UPDATE products set {name}{amt} where id = {Id} ')
    cur.execute(f'UPDATE products SET {name}{amt} where Id = {Id} ')
    conn.commit()
    cur.close()
    conn.close()
    return 'Update Success', 200
    

# create new order
@app.route('/orders', methods=["POST"])
def newOrder():
    pass

# confirm order is complete
@app.route('/completed/<Id>')
def confirmOrder(Id):
    pass

