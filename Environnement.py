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
