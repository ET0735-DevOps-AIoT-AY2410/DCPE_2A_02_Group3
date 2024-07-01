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

# create products given name and amount
@app.route("/newproduct", methods=["POST"])
def createProduct():
    conn=getdb()
    cur=conn.cursor()
    items = ["Name","Quantity"]
    fields= ["Name", "Quantity"] 
    results=[]
    count=0
    for i in items:
        item=request.args.get(i)
        if item ==None:
            return (item + "mising from request"), 400
        results.append("'"+str(item)+"'")
        count+=1
    final='INSERT INTO products('+', '.join(fields)+') VALUES('+','.join(results)+')'
    cur.execute(final)
    conn.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    res=cur.fetchone()
    cur.execute("SELECT * FROM products WHERE Id = "+str(res[0]))
    res=cur.fetchone()
    finalres={
            "id":res[0]
            }
    for i in range(1, len(res)):
        finalres[fields[i-1]]=res[i]
    cur.close()
    conn.close()
    return finalres,200

    


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
    name=("Name = '"+name+"' ") if not name == None else ""
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

