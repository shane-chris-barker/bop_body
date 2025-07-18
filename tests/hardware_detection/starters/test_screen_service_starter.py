import unittest
from unittest.mock import MagicMock, patch
class TestScreenServiceStarter(unittest.TestCase):
    def setUp(self):
        self.pygame_patcher = patch("hardware_detection.starters.screen_service_starter.pygame")
        self.mock_pygame = self.pygame_patcher.start()
        self.addCleanup(self.pygame_patcher.stop)
        self.mock_pygame.init.return_value = None
        self.mock_pygame.quit.return_value = None
        self.mock_pygame.event.get.return_value = []
        self.mock_pygame.time.Clock.return_value = MagicMock()
        from hardware_detection.starters.screen_service_starter import ScreenServiceStarter
        from screen.dtos.screen_message_dto import ScreenMessageDTO
        self.screen_services_starter = ScreenServiceStarter
        self.screen_message_dto = ScreenMessageDTO
        self.starter = self.screen_services_starter(enabled=True)

    def test_cleanup_stops_threads_and_quits(self):
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        self.starter._thread = mock_thread
        self.starter.cleanup()
        self.assertTrue(self.starter._stop_event.is_set())
        mock_thread.join.assert_called_once()
        self.mock_pygame.quit.assert_called_once()

    def test_run_pygame_loop_processes_queue_once(self):
        self.starter._stop_event = MagicMock()
        self.starter._stop_event.is_set.side_effect = [False, True]
        self.starter.screen_updater = MagicMock()
        self.starter._message_queue.put(self.screen_message_dto(message="Bop is putting his face on!", color=(255, 0, 0)))
        self.starter._run_pygame_loop()
        self.mock_pygame.init.assert_called_once()
        self.starter.screen_updater.init_screen.assert_called_once()

    def test_enabled_returns_correctly(self):
        starter = self.screen_services_starter(enabled=False)
        self.assertFalse(starter.enabled())

    def test_stop_stops_thread(self):
        starter = self.screen_services_starter(enabled=True)
        starter._thread = MagicMock()
        starter._thread.is_alive.return_value = False  # Simulate stopped thread
        starter.stop()
        starter._thread.join.assert_called_once()
