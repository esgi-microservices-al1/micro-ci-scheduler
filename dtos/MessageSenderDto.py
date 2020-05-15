from errors.ApiError import ApiError


class MessageSenderDto:

    def __init__(self, message):
        self.message = message


    @staticmethod
    def deserialize(data):
        message = str(data['message'])
        return MessageSenderDto(message)

    def validate(self):
        if self.message is None or self.message is '':
            return False, ApiError(f'name can\'t be None or Empty').serialize()
        return True, None