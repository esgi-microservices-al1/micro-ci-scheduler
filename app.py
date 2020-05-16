from flask import Flask
from flask_restplus import Api

from apis.api_schedule import namespace as schedule_namespace
from apis.api_communication import namespace as communication_namespace

app = Flask(__name__)

api = Api(app, version='1.0', title='Micro-CI-Scheduler API',
          description='a Flask based API for the Micro-CI-Scheduler micro-service')

api.add_namespace(schedule_namespace)
api.add_namespace(communication_namespace)



if __name__ == '__main__':
    app.run()
