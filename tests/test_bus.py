import asyncio
import logging
import pytest
from event_tools import EventBus, Event

# Initialize logger
logger = logging.getLogger(__name__)

@pytest.fixture
def event_bus():
    return EventBus()

@pytest.fixture
def test_event():
    return Event(type="test_event")

@pytest.mark.asyncio
async def test_subscribe(event_bus):
    async def test_handler(event):
        assert event.type == "test_event"

    event_bus.subscribe("test_event", test_handler)
    assert "test_event" in event_bus.subscriptions
    assert test_handler in event_bus.subscriptions["test_event"]

@pytest.mark.asyncio
async def test_remove_subscriber(event_bus):
    async def test_handler(event):
        pass

    event_bus.subscribe("test_event", test_handler)
    event_bus.remove_subscriber(test_handler.__name__, "test_event")
    assert "test_event" in event_bus.subscriptions
    assert test_handler not in event_bus.subscriptions["test_event"]

@pytest.mark.asyncio
async def test_emit(event_bus, test_event):
    event_received = asyncio.Event()

    async def test_handler(event):
        event_received.set()

    event_bus.subscribe("test_event", test_handler)
    await event_bus.emit(test_event)
    assert event_received.is_set()

@pytest.mark.asyncio
async def test_emit_after(event_bus, test_event):
    event_received = asyncio.Event()

    async def test_handler(event):
        event_received.set()

    async def dummy_func():
        pass

    event_bus.subscribe("test_event", test_handler)
    await event_bus.emit_after(test_event, dummy_func)
    assert event_received.is_set()
