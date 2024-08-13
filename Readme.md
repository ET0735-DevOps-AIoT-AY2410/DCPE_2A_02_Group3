# Super cool supermaket system

This project is devloped by 4 students form the class DCPE/2A/02 of AY2024/2025

This is created for the Devops for AIot module.

# Features

there are 4 main systems in this project:
- Raspberry pi
	This handles the self checkout system at the store and the code is stored in `src/`
- MySql DB
	this handles the tracking of stock and orders and is can be created with the script in `backend/createDB.py`
- Backend
	This is a backend written in Flask, which provide apis for the websites and the raspberry pi to get data from the DB

# Running

## Backend

right now, the backend is being hosted on google cloud while the mysql database is hosted on AWS RDS. the google cloud backend is hosted at `https://supermarket-backend-xvd6lpv32a-uc.a.run.app/`

### Running Locally

You can run the backend through the docker or running the python code yourself. All the code for the backend is in `/server/backend/` and you will need the following environments:
``` env
DBHOST=(hostname or ipaddress of mysql databse)
DBUSER=(username to login to mysql database)
DBPASSWORD=(password to login to mysql database)
```
the code will automatically load the environment files

First create the database using `/server/createDB.py` then

you can build the dockerfile in `/server/backend` with `docker build . -t supermarket-system`

then you can run it with `docker run --envfile ./.env supermarket-system`
 
then everything should be working.

you can test the functionality by using pytest on the file `/server/tests/test.py` which would run all the tests

## Frontend

Frontend is ran seperately and can be access through the dockerfile in `http://127.0.0.1:5500/index.html`
(Using Live Server)
Main Website Link: `http://127.0.0.1:5500/Website/index.html`
Cart WebPage Link: `http://127.0.0.1:5500/Website/cart.html`
Login WebPage Link: `http://127.0.0.1:5500/Website/orders.html`
Checkout WebPage Link: `http://127.0.0.1:5500/Website/orders.html`

How does this Website function?
Upon running the website via the live server and pasting the address onto the website, this will bring the customers to the main page of the website

The main page of the website consists of all the available items that allows customers to choose based on their preference
If a customer is intrested to purchase a particular product he/she can click on that particular product
With a click of a button this will bring the customer to the another page which allows them to select the quantity they would like to purchase
Once they are satisfied with the quantity they can simple click on the add to cart icon which allows them to add that product to the cart easily
Once a product has been added to the cart this automatically brings the customer back to the mainpage if they continue to order addtional items
Once all products have been chosen for purchase, the customer can then cart icon to proceed to checkout
The customer can then click the checkout icon which brings them to the checkout page

Customers can choose if they would like to do doorstep delivery
Once everything is done, customers can then click the checkout button which confirms their order
This will bring customers to a qr code page where they can scan the qr code to make payment


navigation across the website is very easy as the icons are alwasy present across the website
If a customer is lost while purchasing through their website they can simply click one of these 3 labels

SPmart - Brings them to the main page
Orders - Shows customers what they have ordered
Cart icon - Shows customers what they have purchased so far

This briefly explains how the website we have created functions


Dockering our website
We have also dockerised this frontend

Docker commands
'docker images' // This command will list all the available images in the container

'docker run -p 5050:80 frontend-website:v2.0'
Name of our image: frontend-website
Tag: v2.0
//Upon executing the command above this will allow the image to run via docker 
## Backende 
