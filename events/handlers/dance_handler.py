import logging
logger = logging.getLogger(__name__)
from bop_common.dtos.event_dto import EventDTO
from events.handlers.event_handler_interface import EventHandlerInterface

class DanceHandler(EventHandlerInterface):
    def __init__(self) -> None:
        self.log_prefix = "[💃 DANCE HANDLER]"

    def handle(self, dto: EventDTO):
        logger.info(f"{self.log_prefix} Bop is dancing!")
        return