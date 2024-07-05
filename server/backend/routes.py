from app import app
from app import getdb
from flask import jsonify,request
from flask_cors import CORS, cross_origin


# get entire list of products database
# GET /products
@app.route("/products", methods=["GET"])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
    cur.execute(f'UPDATE products SET {name}{amt} where Id = {Id} ')
    conn.commit()
    cur.close()
    conn.close()
    return 'Update Success', 200
    

# create new order
@app.route('/orders', methods=["POST"])
@cross_origin()
def newOrder():
    body=request.json
    if body ==None:
        return "please include data",400
    if not "Items" in body:
        return "Please include items",400
    if len(body["Items"])==0:
        return "list cannot be empty"
    if not "Deliver" in body:
        return "include whether it should be delivered"
    conn=getdb()
    cur=conn.cursor()
    paid=1 if body["Deliver"]==1 else 0
    req="INSERT INTO orders(Deliver, Paid, Collected) VALUES("+str(body["Deliver"])+", "+str(paid)+", "+str(paid)+")"
    cur.execute(req)
    conn.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    Id=cur.fetchone()[0]
    for i in body["Items"]:
        req="INSERT INTO orderItems(OrderId, ProductId, Quantity) VALUES("+str(Id)+", "+str(i["itemId"])+", "+str(i["amount"])+")"
        cur.execute(req)
    conn.commit()
    cur.close()
    conn.close()
    return {"orderId":Id},200
    
# read orders
@app.route('/orders', methods=["GET"])
@cross_origin()
def getOrders():
    conn=getdb()
    cur=conn.cursor()
    cur.execute("SELECT * FROM orders")
    allOrders=cur.fetchall()
    final = []
    for i in allOrders:
        order={
            "OrderId":i[0],
            "Deliver":i[1],
            "Paid":i[2],
            "Collected":i[3],
            "Items":[]
        }
        itemsl=[]
        req="SELECT * FROM orderItems WHERE OrderId = "+str(i[0])
        cur.execute(req)
        items=cur.fetchall()
        for i in items:
            itemsl.append({"itemId" : i[1], "quantity" : i[2]})
        order["Items"]=itemsl
        final.append(order)
    return final,200
    
	
# confirm order is complete
@app.route('/collected/<Id>',methods=["PUT"])
@cross_origin()
def confirmOrder(Id):
    req=f'UPDATE orders set Collected = 1 where OrderId = {Id}'
    conn=getdb()
    cur=conn.cursor()
    cur.execute(req)
    conn.commit()
    cur.close()
    conn.close()
    return 'Order updated successfully',200

# confirm order is paid for 
@app.route('/paid/<Id>', methods=["PUT"])
@cross_origin()
def paidOrder(Id):
    req=f'UPDATE orders set Collected = 1 where OrderId = {Id}'
    conn=getdb()
    cur=conn.cursor()
    cur.execute(req)
    conn.commit()
    cur.close()
    conn.close()
    return 'Order updated successfully',200

