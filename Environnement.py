import os


class Environment:

    @staticmethod
    def is_prod_environment():
        if 'ENV' in os.environ and os.environ['ENV'] == 'PROD':
            return True
        return False

    @staticmethod
    def host():
        if 'HOST' in os.environ:
            return os.environ['HOST']
        return None

    @staticmethod
    def port():
        return int(os.environ['PORT'])

    @staticmethod
    def consul_host():
        return os.environ['CONSUL_HOST']

    @staticmethod
    def consul_port():
        return int(os.environ['CONSUL_PORT'])

    @staticmethod
    def consul_token():
        return os.environ['CONSUL_TOKEN']

    @staticmethod
    def amqp_env_variables():
        return { each_env: os.environ[each_env] for each_env in os.environ if 'AMQP' in each_env }

