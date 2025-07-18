import unittest
from unittest.mock import patch, MagicMock
with patch("screen.updaters.screen_updater.pygame") as mock_pygame:
    from screen.updaters.screen_updater import ScreenUpdater
class TestScreenUpdater(unittest.TestCase):

    def setUp(self):
        self.pygame_patcher = patch("screen.updaters.screen_updater.pygame")
        self.mock_pygame = self.pygame_patcher.start()
        self.mock_screen = MagicMock()
        self.mock_font = MagicMock()
        self.mock_text_surface = MagicMock()
        self.mock_pygame.display.set_mode.return_value = self.mock_screen
        self.mock_pygame.font.SysFont.return_value = self.mock_font
        self.mock_font.render.return_value = self.mock_text_surface
        self.mock_pygame.display.flip = MagicMock()
        self.updater = ScreenUpdater()
        self.updater.screen = self.mock_screen

    def test_get_current_message_returns_initial_value(self):
        self.assertEqual(self.updater.get_current_message(), "Bop is putting his best face on!")

    def test_display_text_displays_text(self):
        font = self.mock_font
        self.updater.screen = self.mock_screen
        self.updater.display_text( "Line1\nLine2", (255, 255, 255))
        self.assertEqual(font.render.call_count, 2)
        self.assertEqual(self.mock_screen.blit.call_count, 2)
        self.mock_screen.blit.assert_called()
        self.mock_pygame.display.flip.assert_called()
