import pymongo
import os

client = pymongo.MongoClient("mongodb+srv://" + os.environ['DB_USER'] + ":" + os.environ['DB_PWD'] + "@microservice-schedulerdb-vccyy.azure.mongodb.net/test")
db = client.schedulerdb
