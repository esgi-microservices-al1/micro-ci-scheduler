import os

from rabbitmq import sender
from json import JSONEncoder

from bson import ObjectId
from flask import Flask, request, Response
from flask_restplus import Resource, Api

from dtos.MongoIdDto import MongoIdDto
from dtos.ScheduleCreateDto import ScheduleCreateDto
from dbconnection import db
import pymongo
from models.Schedule import Schedule
from flask import request
from bson.objectid import ObjectId

# subclass JSONEncoder
from dtos.ScheduleDto import ScheduleDto


class DefaultJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


app = Flask(__name__)
app.json_encoder = DefaultJSONEncoder()

api = Api(app, version='1.0', title='Micro-CI-Scheduler API',
          description='a Flask based API for the Micro-CI-Scheduler micro-service')

ns_schedule = api.namespace('schedule', description='schedule operations')
ns_communication = api.namespace('communication', description='communication via amqp operations')


@ns_schedule.route("/")
class ScheduleList(Resource):

    def get(self):
        """
        Fetch all schedules
        """
        schedules = db.Schedule.find()
        list_schedule = []
        for each_schedule in schedules:
            list_schedule.append(ScheduleDto.deserialize(each_schedule))
        encode_list = app.json_encoder.encode(list_schedule)
        response = Response(encode_list, status=200, mimetype='application/json')
        return response

    @api.expect(ScheduleCreateDto.model(api), validate=True)
    def post(self):
        """
        Add a new Schedule
        """
        body = request.get_json()
        schedule_create_dto = ScheduleCreateDto.deserialize(body)
        valid_dto, error = schedule_create_dto.validate()
        if valid_dto is False:
            return error, 400
        inserted = db.Schedule.insert_one(schedule_create_dto.serialize())
        mongo_id_dto = MongoIdDto(str(inserted.inserted_id))
        response = Response(app.json_encoder.encode(mongo_id_dto), status=201, mimetype='application/json')
        response.headers['Location'] = f'{request.base_url}{mongo_id_dto.id}'
        return response


@ns_schedule.route("/<string:id>")
class Schedule(Resource):

    def get(self, id):
        schedule_fetched = db.Schedule.find_one(ObjectId(oid=id))
        schedule_dto = ScheduleDto.deserialize(schedule_fetched)
        response = Response(app.json_encoder.encode(schedule_dto), status=200, mimetype='application/json')
        return response


@ns_communication.route("/")
class Communication(Resource):
    @api.expect(str)
    def post(self):
        sender.send(os.environ['AMQP_IP'],
                    os.environ['AMQP_PORT'],
                    os.environ['AMQP_LOGIN'],
                    os.environ['AMQP_PWD'],
                    os.environ['AMQP_SEND_QUEUE'],
                    'coucou')
        return 'coucou'


@app.route("/schedule/<schedule_id>", methods={'PUT', 'DELETE'})
def put_delete_schedule(schedule_id):
    if not ObjectId.is_valid(schedule_id):
        return 'Invalid schedule id ', 400
    old = db.Schedule.find_one({"_id": ObjectId(schedule_id)})
    if old is None:
        return 'Schedule with id ' + schedule_id + ' not found', 404
    if request.method == 'PUT':
        new = request.get_json()
        old.pop('_id')
        update = {"$set": new}
        db.Schedule.update_one(old, update)
        return 'Schedule updated', 200
    elif request.method == 'DELETE':
        db.Schedule.delete_one(old)
        return 'Schedule deleted', 200


if __name__ == '__main__':
    app.run()
