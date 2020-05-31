from pymongo import MongoClient
from pymongo_inmemory import MongoClient as MemoryMongoClient
import os

if os.getenv('TESTING') is not None and os.environ['TESTING'] == "True":
    print("USING MEMORY")
    client = MemoryMongoClient()
    db = client.schedulerdb
else:
    print("USING ALTAS")
    # db_user = os.environ['DB_USER']
    # db_password = os.environ['DB_PWD']
    # db_host = os.environ['DB_HOST']
    # db_name = os.environ['DB_NAME']
    db_uri = os.environ['DB_URI']
    #f'mongodb+srv://{db_user}:{db_password}@{db_host}/{db_name}'
    client = MongoClient(db_uri)
    db = client.schedulerdb
