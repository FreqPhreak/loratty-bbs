class MessagesView:
    def __init__(self):
        self.inbox = []

    def add(self, msg: str):
        self.inbox.append(str(msg))

    def render(self):
        return "\n".join(self.inbox[-10:])