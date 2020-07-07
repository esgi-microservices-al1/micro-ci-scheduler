import os
import sys

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


def write_cron_env_var():
    file_path = f'{os.path.abspath(os.path.curdir)}/scripts/build_order.env'

    opened = False
    with open(file_path, 'w') as file:
        opened = True
        for each_env, value in Environment.amqp_env_variables().items():
            file.write(f'export {each_env}="{value}"\n')
        file.close()
    if not opened:
        print(f'file path incorrect  : {file_path}', file=sys.stderr)
        exit(0)


if __name__ == '__main__':
    write_cron_env_var()

    if Environment.is_prod_environment():
        consul = ServiceDiscovery()
        consul.register(host=Environment.host(), port=Environment.port(),
                        tags=['queue=al1_scheduled_build', 'traefik.enable=true',
                              'traefik.frontend.entryPoints=http',
                              'traefik.frontend.rule=PathPrefixStrip:/al1.scheduler-ci/'])
    host = Environment.host()
    if Environment.is_prod_environment():
        host = '0.0.0.0'
    app.run(host=host, port=Environment.port())
    if Environment.is_prod_environment():
        consul.deregister()
