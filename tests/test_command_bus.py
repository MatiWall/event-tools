import logging
import pytest
from messaging_tools import CommandBus

# Setting up a logger for testing
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

@pytest.fixture
def command_bus():
    return CommandBus()

def test_register_handler(command_bus):
    # Register a handler
    handler_func = lambda x: x + 1
    command_bus.register_handler("increment", handler_func)
    assert command_bus.handlers["increment"] == handler_func

    # Attempt to register a handler for an existing command type
    with pytest.raises(KeyError) as excinfo:
        command_bus.register_handler("increment", handler_func)
    assert 'Handler for command increment already exists!' in str(excinfo.value)

@pytest.mark.asyncio
async def test_execute(command_bus):
    # Register a handler
    handler_func = lambda x: x + 1
    command_bus.register_handler("increment", handler_func)

    # Execute a command
    res = await command_bus.execute("increment", 5)
    assert res == 6

    # Execute a command with no registered handler
    assert await command_bus.execute("decrement", 5) is None

@pytest.mark.asyncio
async def test_remove_handler(command_bus):
    # Register a handler
    handler_func = lambda x: x + 1
    command_bus.register_handler("increment", handler_func)

    # Remove the handler
    command_bus.remove_handler("increment")
    assert "increment" not in command_bus.handlers

    # Attempt to remove a non-existent handler
    with pytest.raises(KeyError) as excinfo:
        command_bus.remove_handler("decrement")
    assert "No handlers registered for command type: decrement" in str(excinfo.value)
