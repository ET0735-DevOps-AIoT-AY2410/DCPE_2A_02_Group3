import requests
import subprocess
from time import sleep
def test_get_products():
    subprocess.run(["python3", "../createDB.py"]) 
    the_other_process = subprocess.Popen(['python3', '../backend/run.py'])
    response=requests.get("http://localhost:5000/products")
    sleep(2)
    assert response.status_code == requests.codes.ok
    assert response.json()==[]
def test_create_products():
    payload={
            "Name":"Apple", 
            "Quantity":5,
            "Price":5.00,
            "ImageUrl":"amongus"
            }
    response=requests.post("http://localhost:5000/newproduct", params=payload)   
    assert response.status_code==requests.codes.ok
    assert response.json()=={"ImgUrl":"amongus","Name":"Apple","Price":5.0,"Quantity":5,"id":1}
def test_edit_products():
    payload={
            "id":1,
            "Name":"Oranges",
            "Price":6.00,
            "ImageUrl":"amongus2",
            "Quantity":6
            }
    response=requests.put("http://localhost:5000/products", params=payload)   
    print(requests.get("http://localhost:5000/products").json())
    assert response.status_code==requests.codes.ok
    assert response.json()=={"Status": "Update Success"}
    assert requests.get("http://localhost:5000/products").json()==[{
            "id":1,
            "name":"Oranges",
            "price":6.00,
            "imageUrl":"amongus2",
            "quantity":6
            }]
def test_get_orders():
    response=requests.get("http://localhost:5000/orders")
    assert response.status_code == requests.codes.ok
    assert response.json()==[]
def test_create_orders():
    data={
            "Deliver":1,
            "Items":[
                    {
                        "itemId": 1,
                        "amount":3
                        }
                ]
            }
    response=requests.post("http://localhost:5000/orders",json=data)
    assert response.status_code==requests.codes.ok
    assert response.json()=={"orderId":1}
    print(requests.get("http://localhost:5000/orders"))
    assert requests.get("http://localhost:5000/products").json()==[{
            "id":1,
            "name":"Oranges",
            "price":6.00,
            "imageUrl":"amongus2",
            "quantity":3
            }]
    
