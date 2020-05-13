from flask import jsonify


class MongoIdDto:

    def __init__(self, id):
        self.id = id

    def serialize(self):
        return jsonify(self)

    def __str__(self):
        return f'MongoIdDto(id= {self.id})'
