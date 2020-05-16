from flask_restplus import Api, fields


class Message:

    def __init__(self, message):
        self.message = message

    @staticmethod
    def model(api: Api):
        #interval_create_model = IntervalCreateDto.model(api)
        return api.model('message', {
            'message': fields.String(required=True, description='message content')
        })

    def serialize(self):
        return {'message' : self.message}
