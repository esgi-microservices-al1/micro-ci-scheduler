from flask import Flask
from dbconnection import db
import pymongo

app = Flask(__name__)

#MongoDB will create the collection if it does not exist.
print(db)

print(db.())

scheduler_collection = db['schedule']

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/schedule")
def update_schedule():
    schedule = {"name": "John", "address": "Highway 37" }
    inserted = scheduler_collection.insert_one(schedule)
    print(inserted)
    return inserted


if __name__ == '__main__':
    app.run()