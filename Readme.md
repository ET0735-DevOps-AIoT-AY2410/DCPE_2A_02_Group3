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

## Backend
