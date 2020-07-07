from consul import Consul, Check

from Environnement import Environment


class ServiceDiscovery:

    def __init__(self):
        if Environment.is_prod_environment():
            self.consul = Consul(host=Environment.consul_host(), port=Environment.consul_port(),
                                 token=Environment.consul_token(), scheme='http', verify=False)
        else:
            self.consul = Consul(host=Environment.consul_host(), port=Environment.consul_port(),
                                 scheme='http', verify=False)
        self.service_name = 'SchedulerService'

    def register(self, host='localhost', port=3000, tags=None):
        if host is None:
            host = 'localhost'
        self.consul.agent.service.register(name=self.service_name, address=host,
                                           port=port, tags=tags,
                                           check=Check.http(url=f'http://{host}:{port}/check',
                                                            interval=10))

    def deregister(self):

        if Environment.is_prod_environment():
            self.consul.agent.service.deregister(service_id=self.service_name,
                                                 token=Environment.consul_token())
        else:
            self.consul.agent.service.deregister(service_id=self.service_name)
