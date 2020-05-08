from pymongo import MongoClient
import os

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PWD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']

client = MongoClient(f'mongodb://{db_user}:{db_password}@{db_host}/{db_name}')
db = client.schedulerdb

