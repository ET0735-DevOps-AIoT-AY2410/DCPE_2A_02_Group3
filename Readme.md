PURPOSE OF BRANCH
    This branch is used to work on docker. 
    A new branch had to be created in order to remove all picam code and dpednecies from the code as the picam could not be containerised
    The docker works as of the commit that was made to create this readme. 

HOW TO RUN CONTAINER
    First the docker image would need to be buuilt, after cloning the repository use the command: "docker build -t <Desired image name>" 
    This allows the image to be built
    Next run the container using the command docker run --privileged --device /dev/i2c-1 -v /lib/modules:/lib/modules <Previously created image name>
    This command needs to be used instead of a noirmal docker run due to an error a rerlating to the smbus in the hal folder
    While the container is running look at the lcd for instructions on what to do
    ctrl C after the message "thank you have a nice day" appears on the lcd

ISSUES WITH PICAM
    Numerous errors occured when trying to dockerize the picam but an error along the lines of "lib camera not found" was not able to be solved. Methods such as installing using apt/pip was attempted along with cloning from the git repository but the container could not run, however, the image could successfuly build. 