class MessagesView:
    def __init__(self):
        self.inbox = []

    def add(self, msg: str):
        self.inbox.append(str(msg))

    def render(self, height: int):
        # Return only what fits in the given height
        return self.inbox[-height:]