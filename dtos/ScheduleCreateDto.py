from flask_restplus import Api, fields

from dtos.IntervalCreateDto import IntervalCreateDto
from errors.ApiError import ApiError


class ScheduleCreateDto:

    def __init__(self, name, project, branch, interval, start_date):
        self.name = name
        self.project = project
        self.branch = branch
        self.interval = interval
        self.start_date = start_date

    @staticmethod
    def model(api: Api):
        interval_create_model = IntervalCreateDto.model(api)
        return api.model('schedule', {
            'name': fields.String(required=True, description='schedule name'),
            'project': fields.String(required=True, description='project of the schedule'),
            'branch': fields.String(required=True, description='branch of the project'),
            'interval': fields.Nested(interval_create_model, required=True),
            'startDate': fields.DateTime(dt_format='iso8601', required=True)
        })

    @staticmethod
    def deserialize(data):
        interval = IntervalCreateDto.deserialize(data['interval'])
        name = data['name']
        project = data['project']
        branch = data['branch']
        start_date = data['startDate']
        return ScheduleCreateDto(name, project, branch, interval, start_date)

    def serialize(self):
        return {'name': self.name, 'project': self.project,
                'branch': self.branch, 'interval': self.interval.serialize(), 'startDate': self.start_date}

    def validate(self):
        validate_interval, error = self.interval.validate()
        if validate_interval is False:
            return False, error
        elif self.name is None or self.name == '':
            return False, ApiError(f'name can\'t be None or Empty').serialize()
        elif self.project is None or self.project == '':
            return False, ApiError(f'project can\'t be None or Empty').serialize()
        elif self.branch is None or self.branch == '':
            return False, ApiError(f'branch can\'t be None or Empty').serialize()
        return True, None
