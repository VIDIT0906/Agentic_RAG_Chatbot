class MCPQueue:
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)

    def receive(self, receiver):
        for msg in self.messages:
            if msg.receiver == receiver:
                self.messages.remove(msg)
                return msg
        return None

mcp_queue = MCPQueue()