import pytest
from unittest.mock import MagicMock

from bop_common.dtos.event_dto import EventDTO
from bop_common.enums.event_type import EventType
from events.handlers.event_handler_interface import EventHandlerInterface
from events.handlers.handler_registry import HandlerRegistry

class DummyHandlerA(EventHandlerInterface):
    def __init__(self):
        self.name = "DummyHandlerA"
class DummyHandlerB(EventHandlerInterface):
    def __init__(self):
        self.name = "DummyHandlerB"

def make_message_with_input(event_type):
    msg = MagicMock(spec=EventDTO)
    msg.event_type = event_type
    return msg

@pytest.fixture(autouse=True)
def clear_registry_before_tests():
    HandlerRegistry.reset_handlers()
    yield
    HandlerRegistry.reset_handlers()

def test_registry_adds_handler():
    HandlerRegistry.register(EventType.BOP_DANCE, DummyHandlerA)
    assert HandlerRegistry._handlers[EventType.BOP_DANCE] is DummyHandlerA

def test_get_handler_returns_instance_of_registered_handler():
    HandlerRegistry.register(EventType.BOP_HAPPY, DummyHandlerA)
    msg = make_message_with_input(EventType.BOP_HAPPY)
    handler_instance = HandlerRegistry.get_handler_for_message(msg)
    assert isinstance(handler_instance, DummyHandlerA)
    assert handler_instance.name == "DummyHandlerA"

def test_get_handler_raises_if_no_handler_registered():
    msg = make_message_with_input(EventType.BOP_HAPPY)
    with pytest.raises(ValueError) as exception:
        HandlerRegistry.get_handler_for_message(msg)
    assert "No handler registered" in str(exception.value)

def test_register_multiple_handlers_and_resolve():
    HandlerRegistry.register(EventType.BOP_HAPPY, DummyHandlerA)
    HandlerRegistry.register(EventType.BOP_DANCE, DummyHandlerB)

    msg_a = make_message_with_input(EventType.BOP_HAPPY)
    handler_a = HandlerRegistry.get_handler_for_message(msg_a)
    assert isinstance(handler_a, DummyHandlerA)

    msg_b = make_message_with_input(EventType.BOP_DANCE)
    handler_b = HandlerRegistry.get_handler_for_message(msg_b)
    assert isinstance(handler_b, DummyHandlerB)