from pymongo import MongoClient
from pymongo_inmemory import MongoClient as MemoryMongoClient
import os
from flask import Flask
from flask.cli import with_appcontext

app = Flask(__name__)
#
# if not app.config['TESTING']:
#     db_user = os.environ['DB_USER']
#     db_password = os.environ['DB_PWD']
#     db_host = os.environ['DB_HOST']
#     db_name = os.environ['DB_NAME']
#     client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@{db_host}/{db_name}')
#     db = client.schedulerdb
# else:
#     client = MemoryMongoClient()
#     db = client.testdb


if not app.testing:
    print("USING ALTAS")
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PWD']
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@{db_host}/{db_name}')
    db = client.schedulerdb
else:
    print("USING MEMORY")
    client = MemoryMongoClient()
    db = client.testdb
