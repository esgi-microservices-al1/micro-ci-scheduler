from flask_restplus import Resource, Namespace

check_namespace = Namespace('check', description='Health check operations')


@check_namespace.route("")
class Check(Resource):

    def get(self):
        return 'OK', 200
