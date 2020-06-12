import os

from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api
from pymongo_inmemory.downloader import _mkdir_ifnot_exist

from apis.api_schedule import namespace as schedule_namespace
from apis.api_communication import namespace as communication_namespace

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, version='1.0', title='Micro-CI-Scheduler API',
          description='a Flask based API for the Micro-CI-Scheduler micro-service')

api.add_namespace(schedule_namespace)
api.add_namespace(communication_namespace)


print(os.environ.get("PYMONGOIM__BIN_FOLDER", _mkdir_ifnot_exist("bin")))
if __name__ == '__main__':
    app.run(host='0.0.0.0')
