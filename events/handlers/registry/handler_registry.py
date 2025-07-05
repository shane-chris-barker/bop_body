from typing import Dict, Callable
from bop_common.dtos.event_dto import EventDTO
from bop_common.enums.event_type import EventType
from events.handlers.event_handler_interface import EventHandlerInterface

class HandlerRegistry:
    _handlers: Dict[EventType, Callable[[], EventHandlerInterface]] = {}

    @classmethod
    def register(cls, event_type: EventType, factory: Callable[[],EventHandlerInterface]) -> None:
        cls._handlers[event_type] = factory

    @classmethod
    def get_handler_for_message(cls, message: EventDTO) -> EventHandlerInterface:
        factory = cls._handlers.get(message.event_type)
        if factory:
            return factory()
        else:
            raise ValueError(f"No handler registered for event type {message.event_type}")

    @classmethod
    def reset_handlers(cls) -> None:
        cls._handlers.clear()