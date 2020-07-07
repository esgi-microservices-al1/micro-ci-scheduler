# Microservice-Scheduler

Flask API for the micro-ci project.
Micro-CI is a class project carried out as part of our studies at ESGI. If you want to see more about this project click [here](https://github.com/esgi-microservices-al1).


## Requirements
Setup project variables in all .env files and install requirements with :
```shell script
  pip install -r requirements.txt
```

Environment variables needed :
 - DB_USER : database login user
 - DB_PWD : database login password
 - DB_HOST : database address
 - DB_NAME : database name
 - SCRIPTS_PATH : absolute local path of the script folder api on the server 

Requirements to run the scripts/build_order.py :
 - Python 3.7 or later
 - pip installed for all users (`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python get_pyp.py`)

## Usage
```shell script
  py app.py
``` 
or
````shell script
  flask run --host=0.0.0.0
````