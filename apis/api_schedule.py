from bson import ObjectId
from bson.errors import InvalidId
from flask import request, Response
from flask_restplus import Resource, Namespace

from db import db
from dtos.MongoIdDto import MongoIdDto
from dtos.ScheduleCreateDto import ScheduleCreateDto
from dtos.ScheduleDto import ScheduleDto
from errors.ApiError import ApiError
from json_encoder import DefaultJSONEncoder
from tools.crontab_writer import CrontabWriter

namespace = Namespace('schedule', description='schedule operations')

json_encoder = DefaultJSONEncoder()


@namespace.route("")
class ScheduleList(Resource):

    def get(self):
        """
        Fetch all schedules
        """
        schedules = db.Schedule.find()
        list_schedule = []
        for each_schedule in schedules:
            list_schedule.append(ScheduleDto.deserialize(each_schedule))
        encode_list = json_encoder.encode(list_schedule)
        return Response(encode_list, status=200, mimetype='application/json')

    @namespace.expect(ScheduleCreateDto.model(namespace), validate=True)
    def post(self):
        """
        Add a new Schedule
        """
        body = request.get_json()
        schedule_create_dto = ScheduleCreateDto.deserialize(body)
        valid_dto, error = schedule_create_dto.validate()
        if valid_dto is False:
            return error, 400
        try:
            schedule_create_dto.project = ObjectId(oid=schedule_create_dto.project)
        except InvalidId:
            api_error = ApiError(error="invalid ObjectId mongo .")
            return Response(json_encoder.encode(api_error), status=400, mimetype='application/json')

        inserted = db.Schedule.insert_one(schedule_create_dto.serialize())
        mongo_id_dto = MongoIdDto(str(inserted.inserted_id))
        CrontabWriter.add_schedule(schedule_create_dto, str(inserted.inserted_id))
        response = Response(json_encoder.encode(mongo_id_dto), status=201,
                            mimetype='application/json')
        response.headers['Location'] = f'{request.base_url}{mongo_id_dto.id}'
        return response


@namespace.route("/project/<string:project_id>")
@namespace.doc(params={'project_id': 'A project ID'})
class ScheduleProject(Resource):

    @namespace.doc("")
    def get(self, project_id):
        """
        Fetch schedules of a given project
        """
        try:
            ObjectId(oid=project_id)
        except InvalidId:
            api_error = ApiError(error="invalid ObjectId mongo .")
            return Response(json_encoder.encode(api_error), status=400, mimetype='application/json')

        schedules_found = db.Schedule.find({"project": ObjectId(oid=project_id)})
        list_schedule = []
        for each_schedule in schedules_found:
            list_schedule.append(ScheduleDto.deserialize(each_schedule))
        encode_list = json_encoder.encode(list_schedule)
        return Response(encode_list, status=200, mimetype='application/json')


@namespace.route("/<string:id>")
@namespace.doc(params={'id': 'A schedule ID'})
class Schedule(Resource):

    def get(self, id):
        """
        Fetch schedule by schedule ID
        """
        schedule_fetched = db.Schedule.find_one(ObjectId(oid=id))

        schedule_dto = ScheduleDto.deserialize(schedule_fetched)
        response = Response(json_encoder.encode(schedule_dto), status=200,
                            mimetype='application/json')
        return response

    @namespace.expect(ScheduleCreateDto.model(namespace), validate=True)
    def put(self, id):
        """
        Update schedule by schedule ID
        :param id:
        :return:
        """
        if not ObjectId.is_valid(id):
            return 'Invalid schedule id ', 400
        old = db.Schedule.find_one({"_id": ObjectId(id)})
        if old is None:
            return 'Schedule with id ' + id + ' not found', 404
        new = request.get_json()
        old.pop('_id')
        update = {"$set": new}
        db.Schedule.update_one(old, update)
        CrontabWriter.update_schedule(old_schedule=old, old_id=id,
                                      new_schedule=ScheduleCreateDto.deserialize(new), new_id=id)
        return 'Schedule updated', 200

    def delete(self, id):
        if not ObjectId.is_valid(id):
            return 'Invalid schedule id ', 400
        old = db.Schedule.find_one({"_id": ObjectId(id)})
        if old is None:
            return 'Schedule with id ' + id + ' not found', 404
        db.Schedule.delete_one(old)
        CrontabWriter.update_schedule(old_schedule=old, old_id=id)
        return 'Schedule deleted', 200
