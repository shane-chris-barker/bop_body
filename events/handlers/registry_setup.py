from bop_common.enums.event_type import EventType
from events.handlers.dance_handler import DanceHandler
from events.handlers.happy_handler import HappyHandler
from events.handlers.handler_registry import HandlerRegistry

def register_handlers():
    HandlerRegistry.register(EventType.BOP_DANCE, DanceHandler)
    HandlerRegistry.register(EventType.BOP_HAPPY, HappyHandler)