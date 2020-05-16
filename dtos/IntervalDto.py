

class IntervalDto:

    def __init__(self, unity, frequency):
        self.unity = unity
        self.frequency = frequency

    @staticmethod
    def deserialize(data):
        unity = data['unity']
        frequency = data['frequency']
        return IntervalDto(unity, frequency)

