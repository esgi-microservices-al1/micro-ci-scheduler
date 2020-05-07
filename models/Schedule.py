class Schedule:
    def __init__(self, _id, name, project, branch, interval, startDate):
        self._id = _id
        self.name = name
        self.project = project
        self.branch = branch
        self.interval = interval
        self.startDate = startDate

    def serialize(self):
        return {"_id": self._id, "name": self.name, "project": self.project, "branch": self.branch,
                "interval": self.interval.serialize(), "startDate": self.startDate}
