import unittest
from unittest.mock import patch, MagicMock

with patch("screen.screen_updater.pygame") as mock_pygame:
    from screen.screen_updater import ScreenUpdater
    from screen.dtos.screen_message_dto import ScreenMessageDTO

class TestScreenUpdater(unittest.TestCase):

    def setUp(self):
        self.mock_pygame = patch("screen.screen_updater.pygame").start()
        self.addCleanup(patch.stopall)
        self.mock_screen = MagicMock()
        self.mock_font = MagicMock()
        self.mock_text_surface = MagicMock()
        self.mock_pygame.display.set_mode.return_value = self.mock_screen
        self.mock_pygame.font.SysFont.return_value = self.mock_font
        self.mock_font.render.return_value = self.mock_text_surface
        self.mock_pygame.event.get.return_value = []
        self.mock_pygame.display.flip = MagicMock()
        self.updater = ScreenUpdater(enabled=True)
        self.updater.screen = self.mock_screen


    def test_display_text_queues_and_renders(self):
        test_message = "TEST"
        test_color = (255,255,255)
        dto = ScreenMessageDTO(test_message, test_color)
        self.updater.display_text(dto.message, dto.color)

        queued = self.updater._message_queue.get_nowait()
        self.assertEqual(queued.message, dto.message)
        self.assertEqual(queued.color, dto.color)

        self.mock_screen.fill.assert_called_with((0,0,0))
        self.mock_font.render.assert_called_with(test_message, True, test_color)
        self.mock_screen.blit.assert_called_with(self.mock_text_surface, (50, 150))
        self.mock_pygame.display.flip.assert_called_once()

    def test_enabled_flag_blocks_display_text(self):
        updater = ScreenUpdater(enabled=False)
        updater.display_text("I should not be displayed")
        self.assertTrue(updater._message_queue.empty())

    def test_get_current_message_returns_initial_value(self):
        self.assertEqual(self.updater.get_current_message(), "Bop is putting his best face on!")

    def test__render_text_renders_multiline(self):
        font = self.mock_font
        self.updater.screen = self.mock_screen
        self.updater._render_text(font, "Line1\nLine2", (255, 255, 255))
        self.assertEqual(font.render.call_count, 2)
        self.assertEqual(self.mock_screen.blit.call_count, 2)
        self.mock_pygame.display.flip.assert_called()

    def test_cleanup_stops_threads_and_quits(self):
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        self.updater._pygame_thread = mock_thread
        self.updater.cleanup()
        self.assertTrue(self.updater._stop_event.is_set())
        mock_thread.join.assert_called_once()
        self.mock_pygame.quit.assert_called_once()

    def test_start_does_nothing_if_disabled(self):
        updater = ScreenUpdater(enabled=False)
        updater.start()
        self.assertIsNone(updater._pygame_thread)

    def test__run_pygame_loop_processes_queue_once(self):
        mock_screen = MagicMock()
        mock_font = MagicMock()
        mock_surface = MagicMock()

        self.mock_pygame.display.set_mode.return_value = mock_screen
        self.mock_pygame.font.SysFont.return_value = mock_font
        mock_font.render.return_value = mock_surface
        self.mock_pygame.event.get.return_value = []

        updater = ScreenUpdater(enabled=True)
        updater._stop_event = MagicMock()
        updater._stop_event.is_set.side_effect = [False, True]
        updater._message_queue.put(ScreenMessageDTO("Bop is putting his best face on!", (255, 255, 255)))
        updater._run_pygame_loop()

        mock_font.render.assert_called_with("Bop is putting his best face on!", True, (255,255,255))
        mock_screen.blit.assert_called()
        self.mock_pygame.display.flip.assert_called()

    def test_enabled_flag_blocks_start(self):
        updater = ScreenUpdater(enabled=False)
        updater.start()
        self.assertIsNone(updater._pygame_thread)

    def test_display_text_init_pygame_if_needed(self):
        self.mock_pygame.get_init.return_value = False
        self.mock_pygame.font.get_init.return_value = False
        message = "Init Check"
        self.updater.display_text(message, (255, 255, 255))
        self.mock_pygame.init.assert_called()
        self.mock_pygame.font.init.assert_called()

