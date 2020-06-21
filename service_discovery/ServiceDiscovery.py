from consul import Consul, Check

from Environnement import Environment


class ServiceDiscovery:

    def __init__(self):
        self.consul = Consul(host=Environment.consul_host(), port=Environment.consul_port(),
                             scheme='http', verify=False)
        self.agent = self.consul.Agent(agent=self.consul)
        self.service_name = 'SchedulerService'

    def register(self, host='localhost', port=3000, tags=None):
        if host is None:
            host = 'localhost'

        print(self.agent.services())
        self.agent.service.register(name=self.service_name, address=host,
                                    port=port, tags=tags,
                                    check=Check.http(url=f'http://{host}:{port}/check',
                                                     interval=10))

    def deregister(self):
        self.agent.service.deregister(service_id=self.service_name)
