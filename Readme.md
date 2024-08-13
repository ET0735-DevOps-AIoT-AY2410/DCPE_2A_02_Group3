# SP Mart Supermarket Self-Checkout System

This project is devloped by 4 students form the class DCPE/2A/02 of AY2024/2025

This is created for the Devops for AIot module.

# Work Distribution
- Chandan <br>
Website homepage <br>
Dockerizing Website <br>

- Jerick <br>
Cloud SQL database <br>
APIs to communicate with DB <br>
Fixes in web site code <br>
QR code payment page <br>

- Mingfeng<br>
Shopping cart<br>
Admin Page<br>

- Paven <br>
All RPI code/functionality <br>
Dockerizing RPI <br>

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

Frontend is ran seperately and can be access through the dockerfile in `http://127.0.0.1:5500/index.html` <br>
(Using Live Server)
Main Website Link: `http://127.0.0.1:5500/Website/index.html` <br>
Cart WebPage Link: `http://127.0.0.1:5500/Website/cart.html` <br>
Login WebPage Link: `http://127.0.0.1:5500/Website/orders.html` <br>
Checkout WebPage Link: `http://127.0.0.1:5500/Website/orders.html` <br>

How does this Website function? <br>
Upon running the website via the live server and pasting the address onto the website, this will bring the customers to the main page of the website <br>

The main page of the website consists of all the available items that allows customers to choose based on their preference <br>
If a customer is intrested to purchase a particular product he/she can click on that particular product <br>
With a click of a button this will bring the customer to the another page which allows them to select the quantity they would like to purchase <br>
Once they are satisfied with the quantity they can simple click on the add to cart icon which allows them to add that product to the cart easily <br>
Once a product has been added to the cart this automatically brings the customer back to the mainpage if they continue to order addtional items <br>
Once all products have been chosen for purchase, the customer can then cart icon to proceed to checkout <br>
The customer can then click the checkout icon which brings them to the checkout page <br>

Customers can choose if they would like to do doorstep delivery <br>
Once everything is done, customers can then click the checkout button which confirms their order <br>
This will bring customers to a qr code page where they can scan the qr code to make payment <br>


navigation across the website is very easy as the icons are alwasy present across the website <br>
If a customer is lost while purchasing through their website they can simply click one of these 3 labels <br>

SPmart - Brings them to the main page <br>
Orders - Shows customers what they have ordered <br>
Cart icon - Shows customers what they have purchased so far <br>

This briefly explains how the website we have created functions <br>


Dockering our website <br>
We have also dockerised this frontend <br>

Docker commands <br>
'docker images' // This command will list all the available images in the container <br>

'docker run -p 5050:80 frontend-website:v2.0' <br>
Name of our image: frontend-website <br>
Tag: v2.0 <br>
//Upon executing the command above this will allow the image to run via docker <br>

## Rasberry Pi

### Hardware Requirements
Uses a RPI 4 with multiple modules including  
- Picamera ->  used for deocding barcode and qr code
- RFID module -> used for payment functionality by interfacing with csv database
- Keypad ->  Used for payment in pin requriment by inputting pin number
- 16x2 LCD -> General use in displaying instructions for user to interact

### Software requirements & Running code

Code can be ran as a docker container or running the code natively

1. Running as a docker container

- First you would need to pull from the dockerhub which is currently a public repository titled "dcpe_2a02_group3_dockerhub". 
- Pull this image onto your computer using "Docker Pull"
- Next to run the the image you need to use the docker command "docker run --privileged --device /dev/i2c-1 -v /lib/modules:/lib/modules -t _image name_ " 
- This will run the docker container, while the code is running refer to the LCD screen for insturctions

2. Running the code natively

- Assuming you have met the hardware requirments use the git clone command with submodules "git clone --recurse-submodules _repo url from git hub_".
- Next install all modules imported, which i will not be listing and run the code. 
- Ensure that your RPI is configured to not use legacy camera which refers to picam and not picam2 
- Run main.py and look at the terminal or LCD for instructions. 