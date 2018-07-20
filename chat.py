import json

class Chat:
    channel = ""
    user = ""
    message = ""
    time = ""

    def __init__(self, channel, user, message, time):
        self.channel = channel
        self.user = user
        self.message = message
        self.time = time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def newChat(channel, user, message, time):
    chat = Chat(channel, user, message, time)
    return chat