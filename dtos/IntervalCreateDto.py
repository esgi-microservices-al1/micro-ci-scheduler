from flask_restplus import fields, Namespace

from errors.ApiError import ApiError


class IntervalCreateDto:

    def __init__(self, unity, frequency):
        self.unity = unity
        self.frequency = frequency

    @staticmethod
    def model(namespace: Namespace):
        return namespace.model('interval', {
            'unity': fields.String(required=True, description='unity of the interval'),
            'frequency': fields.Integer(required=True, description='frequency of the interval')
        })

    @staticmethod
    def deserialize(data):
        unity = data['unity']
        frequency = data['frequency']
        return IntervalCreateDto(unity, frequency)

    def serialize(self):
        return {'unity' : self.unity, 'frequency' : self.frequency}

    def validate(self):
        if self.unity == 'DAY' and self.frequency < 1:
            return False, ApiError(f'interval.frequency shouldn\'t be {self.frequency}').serialize()
        return True,None
