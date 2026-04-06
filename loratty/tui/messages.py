class MessagesView:
    def __init__(self):
        self.inbox = []

    def add(self, msg):
        self.inbox.append(msg)

    def render(self):
        return "\n".join(self.inbox[-10:])