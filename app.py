import os

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from Environnement import Environment
from service_discovery.ServiceDiscovery import ServiceDiscovery

from apis.api_schedule import namespace as schedule_namespace
from apis.api_communication import namespace as communication_namespace
from apis.api_check import check_namespace

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, version='1.0', title='Micro-CI-Scheduler API',
          description='a Flask based API for the Micro-CI-Scheduler micro-service')

api.add_namespace(schedule_namespace)
api.add_namespace(communication_namespace)
api.add_namespace(check_namespace)


if __name__ == '__main__':
    print(os.environ)
    consul = ServiceDiscovery()
    consul.register(host=Environment.host(), port=Environment.port(),
                    tags=['queue=al1_scheduled_build'])
    host = Environment.host()
    if Environment.is_prod_environment():
        host = '0.0.0.0'
    app.run(host=host, port=Environment.port())
    consul.deregister()
