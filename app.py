from flask import Flask
from dbconnection import db
import pymongo
from models.Schedule import Schedule
from flask import request
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/schedule/<schedule_id>", methods={'PUT'})
def put_schedule(schedule_id):
    if not ObjectId.is_valid(schedule_id):
        return 'Invalid schedule id ', 400
    old = db.Schedule.find_one({"_id": ObjectId(schedule_id)})
    if old is None:
        return 'Schedule with id ' + schedule_id + ' not found', 404
    new = request.get_json()
    old.pop('_id')
    update = {"$set": new}
    db.Schedule.update_one(old, update)
    return 'Schedule updated', 200


if __name__ == '__main__':
    app.run()
