from dtos.IntervalDto import IntervalDto


class ScheduleDto:

    def __init__(self, id, name, project, branch, interval, start_date):
        self.id = id
        self.name = name
        self.project = project
        self.branch = branch
        self.interval = interval
        self.start_date = start_date

    @staticmethod
    def deserialize(data):
        interval = IntervalDto.deserialize(data['interval'])
        id = str(data['_id'])
        name = data['name']
        project = data['project']
        branch = data['branch']
        start_date = data['startDate']
        return ScheduleDto(id, name, project, branch, interval, start_date)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and \
               self.project == other.project and self.branch == other.branch and \
               self.interval == other.interval and self.start_date == other.start_date
