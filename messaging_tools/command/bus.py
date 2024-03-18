import logging
import asyncio
from typing import Callable

logger = logging.getLogger(__name__)

class CommandBus:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, command_type, handler):
        if command_type not in self.handlers:
            self.handlers[command_type] = handler
        else:
            raise KeyError(f'Handler for command {command_type} already exists!')

    def remove_handler(self, command_type):
        if command_type in self.handlers:
            del self.handlers[command_type]
        else:
            raise KeyError(f"No handlers registered for command type: {command_type}")

    async def execute(self, command_type, *args, **kwargs):
        try:
            handler = self.handlers[command_type]
            return await self._run(handler, *args, **kwargs)
        except KeyError as e:
            logger.exception(f'No handler exists for command {command_type}')
            return None
        except Exception as e:
            logger.exception(f'Handling command {command_type} failed with error: \n')


    async def _run(self, func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return await asyncio.to_thread(func, *args, **kwargs)
