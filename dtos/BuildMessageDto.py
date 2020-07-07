class BuildMessageDto:
    def __init__(self, project, branch):
        self.project = project
        self.branch = branch

    def encode_to_json(self):
        return '{ \"project\": \"' + self.project + \
               '\", \"branch\": "' + self.branch + '\" }'
