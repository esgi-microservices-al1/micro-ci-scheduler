# docker-compose Micro-CI-Scheduler

Launch all services with:

````shell script
docker-compose up -d
````

## Micro-CI Scheduler

The python Flask based API for the Scheduler Micro-service

see all apis : http://127.0.0.1:5000/

## MongoDB (Production Mode)

We use a Replica Set Mongo DB instances. 

1 Primary instance (Read + Write) and 2 Secondary instances (Read)

### Replica Set configuration

```shell script
docker exec -it mongo1 mongo -u username

password (it will be asked)

config={_id:"mongo-replSet",members:[{_id:0,host:"mongo1:27017"},{_id:1,host:"mongo2:27017"},{_id:2,host:"mongo3:27017"}]};

rs.initiate(config);

exit
```

### Connexion URI to Replica Set

The scheduler Micro-service should connect to the mongoDB Replica Set with the URI string here

````shell script
DB_URI=mongodb://username:password@mongo1,mongo2,mongo3/?replicatSet=mongo-replSet&eadPreference=secondary
````

## RabbitMQ (Production Mode)
Here a brief description