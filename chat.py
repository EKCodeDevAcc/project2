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

def newChat(channel, user, message, time):
    chat = Chat(channel, user, message, time)
    return chat