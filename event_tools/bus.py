import logging
logger = logging.getLogger(__name__)

import asyncio
from asyncio import coroutines
from typing import Callable

from event_tools.events import Event
class EventBus:
    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        self.subscriptions[event_type].append(handler)

    def remove_subscriber(self, handler_name, event_type):

        event_handlers_copy = self.subscriptions[event_type].copy()

        for func in self._event_handlers(event_type):
            if func.__name__ == handler_name:
                event_handlers_copy.remove(func)

        if self.subscriptions[event_type] == event_handlers_copy:
            logger.warning(f'Handler {handler_name} does not exists in subscribers.')
        else:
            self.subscriptions[event_type] = event_handlers_copy

    async def emit(self, event):
        handlers = self.subscriptions.get(event.type, [])
        coroutines = []
        for handler in handlers:
            coroutines.append(self._run(handler))
        await asyncio.gather(*coroutines)

    async def emit_after(self, event: Event, func: Callable, *args, **kwargs):
        res = await func(*args, **kwargs)
        await self.emit(event)
        return res

    async def _run(self, func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            res = await func(*args, **kwargs)
        else:
            res = await asyncio.to_thread(func, *args, **kwargs)
        return res

    def _event_handlers(self, event_type):
        for handler in self.subscriptions[event_type]:
            yield handler

    def _event_handler_names(self, event_type):
        return [handler.__name__ for handler in self.subscriptions[event_type]]


