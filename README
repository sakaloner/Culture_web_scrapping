This is a python project that consists of scripts to download and save
the content of several csv files from a webpage to a local posgtresql 
database.

###
To locally run this project you need python (I developed and tested)
the project with python 3.10 but I dont see why any other python3
interpreter would not work.
Create a virtual environment if you wish, activate it and then run
the command:
Install the requirements by doing:
```
pip install -r requirements.txt
```
this command will install all the python libraries we need for running
the project.
Then create a .env file as in the .env example here in the repository.
The next step is to make sure you have docker installed and you are not running
a postgresql server in your local machine in the same ports as chosen
in the .env file.

Start the container with either docker-compose up -d for windows
or docker compose up -d for a linux based machine.
(This project, the docker container and python scripts works either
on a python or a linux machine)

After the containers are initialized the postgres sql databse would
have been created with the tables we need to populate the data
from the goverment website, you can change the sql code in the 
script_db folder to create another initialization setup.
This sql script will start only if the posgres server cant find
another database. So it would generally just run once because the docker
container have a persistent volume to save data. 
To erase the volume to test the initialization script again you can
erase the docker volume associeted with the these images by doing in a linux machine 
```
docker volume rm $(docker volume ls -q) 
```

After launching the docker container you can check if the connection is ready
by either reading the docker logs or with the UI webpage admin 
script (the adminer service).

When the postgres server is ready you can start the python workflow
by running the main.py in the challenge_code directory.

Theres a jupyter notebook file called "cleaning_data" in the challenge_code
directory to test the data manipulation data the data_filter creates

