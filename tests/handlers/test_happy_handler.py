import unittest
from unittest.mock import MagicMock
from events.handlers.happy_handler import HappyHandler
from bop_common.dtos.event_dto import EventDTO
from bop_common.enums.event_type import EventType

class TestHappyHandler(unittest.TestCase):
    def setUp(self):
        self.mock_screen_updater = MagicMock()
        self.handler = HappyHandler(screen_updater=self.mock_screen_updater)
        self.dto = EventDTO(event_type=EventType.BOP_HAPPY)

    def test_handle_calls_display_text(self):
        self.handler.handle(self.dto)
        self.mock_screen_updater.display_text.assert_called_once_with("Bop is happy!")