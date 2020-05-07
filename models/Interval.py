class Interval:
    def __init__(self, unity, frequency):
        self.unity = unity
        self.frequency = frequency

    def serialize(self):
        return {"unity": self.unity, "frequency": self.frequency}