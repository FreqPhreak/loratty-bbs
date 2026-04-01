import asyncio

class EventBus:
    def __init__(self):
        self.listeners = {}

    def on(self, event_name, callback):
        """Register an event listener."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def emit(self, event_name, data):
        """Emit an event to all listeners."""
        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:
            asyncio.create_task(callback(data))