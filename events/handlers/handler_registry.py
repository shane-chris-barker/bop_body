from typing import Dict, Type
from bop_common.dtos.event_dto import EventDTO
from bop_common.enums.event_type import EventType
from events.handlers.event_handler_interface import EventHandlerInterface

class HandlerRegistry:
    _handlers: Dict[EventType, Type[EventHandlerInterface]] = {}

    @classmethod
    def register(cls, event_type: EventType, handler_cls: Type[EventHandlerInterface]) -> None:
        cls._handlers[event_type] = handler_cls

    @classmethod
    def get_handler_for_message(cls, message: EventDTO) -> EventHandlerInterface:
        handler_cls = cls._handlers.get(message.event_type)
        if handler_cls:
            return handler_cls()
        else:
            raise ValueError(f"No handler registered for event type {message.event_type}")

    @classmethod
    def reset_handlers(cls) -> None:
        cls._handlers.clear()