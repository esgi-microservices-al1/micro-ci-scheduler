

class ApiError:

    def __init__(self, error):
        self.message = error

    def serialize(self):
        return { "message" : self.message }
