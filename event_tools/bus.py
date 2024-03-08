

class EventBus:
    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        self.subscriptions[event_type].append(handler)

    async def publish(self, event):
        handlers = self.subscriptions.get(event.type, [])
        coroutines = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                coroutines.append(handler(event))
            else:
                coroutines.append(asyncio.to_thread(handler, event))
        await asyncio.gather(*coroutines)