import logging
logger = logging.getLogger(__name__)
from bop_common.dtos.event_dto import EventDTO
from events.handlers.event_handler_interface import EventHandlerInterface
from screen.updaters.screen_updater import ScreenUpdater

class SadHandler(EventHandlerInterface):
    def __init__(self, screen_updater: ScreenUpdater) -> None:
        self.log_prefix = "[🥹 SAD HANDLER]"
        self.screen_updater = screen_updater

    def handle(self, dto: EventDTO) -> None:
        logger.info(f"{self.log_prefix} Bop is sad...")
        self.screen_updater.display_text("Bop is sad...")
        return
