
# General description of server

the general layout of the server is that we are going to be using mysql database connected to flask for the backend. We will also be using RESTful api to access the database. so basically what it means it that there will be many urls and you just call them for the different functionalities

## Databases

In the sql database, if `createDB.py` is ran, it will create the neccessary databases and tables needed for the code.

For SQL, the layout is as follows, there is one database and many tables inside the database. you can think of it as an excel file with the database being the file itself and the tables inside being tabs inside the excel file.

So for our project, I have created the database "supermarket" and within it there are 3 tables:
1. products
2. orders
3. orderItems
Products contains the id, name and quantity of each product we have in stock.

Orders contains the id of the order, whether it is a delivered item, whether it is paid for and whether it has been collected.

OrderItems contain the items in each order. they can be identified by the orderid in the table "Orders". it contains the orderid of the item, item name and amount of item.



---

# What is an api call?

You do api calls everyday. Whenever you access the website, you make an api call, and inside the website itself, many more calls are made to serve you ads, get images, load comments so on and so forth. 
So what IS an api?
apis can be broken down into the simplest form which is:
```GET https://youtube.com```
a verb in this case `GET` and a url in this case `https://youtube.com`
the verb can be many things and if you want to read more you can do so at https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods 
other those 2 links, you can include querys and body

### Queries

queries are placed directly after the url as in:
```https://www.youtube.com/watch?v=dQw4w9WgXcQ```
where the query is the part after the question mark, where you can put in a variable in this case it sets the variable `v` to `dQw4w9WgXcQ`.

### Body

The body is more information you can add to the call to transfer data as it may be unsightly to see such a long url in the taskbar. This data can be anything from binary to json 


---

# Endpoints

When I describe how to use the endpoint I will do so by omitting the base path of the url for example for `https://youtube.com/watch/` it will become `/watch`. I will also add the http verb for each.

## Products

### Get Products

```GET /Products```
nothing else needed.
will return the following:
```
[
	{
		"id":(Item id as int),
		"name":(name of product as string),
		"quantity":(amount of product as int)
	}
]
```
as an example it may return:
```
[
    {
        "id": 1,
        "name": "apple",
        "quantity": 5
    },
    {
        "id": 2,
        "name": "orange",
        "quantity": 6
    }
]
```

### Create Product
creates new product
```POST /newproduct?Name=(String)&Quantity=(Int)```
at minimum include in query name and quantity of the product for example you can call it like this:
```POST /newproduct?Name=Apple&Quantity=5```
it will return the same product in the following format:
```{
    "Name": (String),
    "Quantity": (Int),
    "id": (Int)
}```
for example it will return the following:
```{
    "Name": "Apple",
    "Quantity": 5,
    "id": 3
}```

### edit products
edit fields of product e.g quantity or name
```PUT /products?id=(int)```
the minimum is that a id query is needed. and after that, name and amount has to be added to facilitate changes to the id of the product itself.
for example you can call it like so:
```PUT /prodcuts?id=1&Quantity=4```
which would update the quantity of item at id 1 to 4.
this would just output `Update success if successful`

## Orders

this specifies orders from the website both delivery and onsite collection

### Get Orders
gets orders currently
```GET /orders```
will return in the following format:
```
{
    "OrderId":(Int id of order),
    "Deliver":(Int 1 if order should be delivered),
    "Paid":(Int 1 if paid already),
    "Collected":(Int 1 if collected already),
    "Items":[
	{
	    "itemId":(Id of item as Int),
	    "quantity":(Int amount of item)
	}
    ]
}
```
for example it can return:
```
[
    {
        "Collected": 1,
        "Deliver": 0,
        "Items": [
            {
                "itemId": 1,
                "quantity": 2
            },
            {
                "itemId": 2,
                "quantity": 3
            }
        ],
        "OrderId": 1,
        "Paid": 0
    }
]
```

### Create Order

creates order giving items and whether it should be delivered or not
```POST /orders```
need to include the following data into body of api call:
```
{
    "Deliver":(Int 1 if it should be delivered),
    "Items":[
        {
            "itemId":(Int id of item in order),
            "amount":(Int amount of item in order)
        }
    ]
}
```
as example you can pass in the following:
```
{
    "Deliver":0,
    "Items":[
        {
            "itemId":1,
            "amount":2
        },
        {
            "itemId":2,
            "amount":3
        }
    ]
}
```
when created for delivery, the `Paid` and `Collected` fields will be set to 1 as it is delivery.
if `delivery` is set to 0, `Paid` and `Collected` fields will also be set to 0 as collection requires it.
and it will return the following:
```
{
"orderId":(Int of id of order)
}
```

### Completed order

marke order as collected
```PUT /collected/<Id>``` where you replace `<Id>` with id of order
this will mark it as collected by changing the value of collected to 1
will return `Order updated successfully`

### paid for order

marke order as paid for
```PUT /paid/<Id>``` where you replace `<Id>` with id of order
this will mark it as paid for by changing the value of collected to 1
will return `Order updated successfully`

---
# How should I call the api?
## Front end (js)
https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch 
just use this
or you can use `fetch(url).then(response=>{})` but this exercise is left to the reader to find out
