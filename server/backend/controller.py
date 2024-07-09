from app import app
from app import getdb
from flask import jsonify,request
def controlGetProducts():
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
                    "price":i[2],
                    "imageUrl":i[3],
                    "quantity":i[4]
                    })
    cur.close()
    conn.close()
    return jsons

def controlgetproduct(id):
    conn=getdb()
    cur=conn.cursor()
    cur.execute("SELECT * FROM products WHERE Id = "+str(id))
    res=cur.fetchone()
    cur.close()
    conn.close()
    return res

def controlCreateProduct(name,price,imageurl,amt):
    fields= ["Name", "Price", "ImgUrl", "Quantity"] 
    results=[]
    count=0
    for i in [name,price,imageurl,amt]:
        item=i
        if item ==None:
            return (i + " missing from request"), 400
        results.append("'"+str(item)+"'")
        count+=1
    conn=getdb()
    cur=conn.cursor()
    final='INSERT INTO products('+', '.join(fields)+') VALUES('+','.join(results)+')'
    print(final)
    cur.execute(final)
    conn.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    id=cur.fetchone()[0]
    cur.close()
    conn.close()
    res=controlgetproduct(id)
    finalres={
            "id":controlgetproduct(res)
            }
    for i in range(1, len(res)):
        finalres[fields[i-1]]=res[i]
    
    return finalres,200

def controlEditProduct(id, changes):
    conn=getdb()
    cur=conn.cursor()
    final=[]
    for i in changes.keys():
        final.append(i+ " = '"+str(changes[i])+"'")
    finals=f'UPDATE products SET {", ".join(finals)} where Id = {id} '
    cur.execute(finals)
    conn.commit()
    cur.close()
    conn.close()
    return True