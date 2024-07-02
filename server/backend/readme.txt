ok so right guys if you want to run the server you have to do the following things
1. make sure mysql is installed
2. create ".env" text file in server folder and include the following things:
	DBUSER={insert username of mysql here in quotes}
	DBPASSWORD={insert password of mysql here in quotes}
if not you will get some error about os or dotenv or smt like that
3. install flask
4. when in the server folder in your command line, run:
	flask --app run.py run
and it should run
let jerick know if there are any problems
