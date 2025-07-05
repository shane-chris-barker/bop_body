import logging
import queue
import threading
from typing import Tuple
logger = logging.getLogger(__name__)
import pygame
from screen.dtos.screen_message_dto import ScreenMessageDTO
from hardware_detection.services.device_service_interface import DeviceServiceInterface

class ScreenUpdater(DeviceServiceInterface):
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = enabled
        self.screen = None
        self._pygame_thread = None
        self._stopEvent = threading.Event()
        self._message_queue = queue.Queue()
        self._stop_event = threading.Event()
        self.log_prefix = "[📺 SCREEN UPDATER]"
        self._current_color = (255, 255, 255)
        self._current_message = "Bop is putting his best face on!"

    def start(self) -> None:
        if not self._enabled:
            return
        logger.info(f"{self.log_prefix} is initializing the screen.")
        self._stop_event.clear()
        self._pygame_thread = threading.Thread(target=self._run_pygame_loop, daemon=True)
        self._pygame_thread.start()

    def _run_pygame_loop(self) -> None:
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            font = pygame.font.SysFont("Arial", 36)
            self._render_text(font, self._current_message, self._current_color)
            clock = pygame.time.Clock()

            while not self._stop_event.is_set():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        logger.info(f"{self.log_prefix} Bop's face is shutting down")
                        self._stop_event.set()
                        break
                try:
                    message_data = self._message_queue.get_nowait()
                    self.current_color = message_data.color
                    self.current_message = message_data.message
                    self._render_text(font, self.current_message, self.current_color)
                except queue.Empty:
                    pass
                clock.tick(30)
            pygame.quit()
            logger.info(f"{self.log_prefix} Bop's face is shutting down")
        except Exception as e:
            logger.error(f"{self.log_prefix} Error in pygame - {e}")
            if 'pygame' in locals():
                pygame.quit()

    def _render_text(self, font, message: str, color: Tuple[int, int, int]) -> None:
        if not self.screen:
            return
        self.screen.fill((0, 0, 0))
        lines = message.split("\n")
        y_offset = 150
        line_height = 40
        for line in lines:
            if line.strip():
                text_surface = font.render(line, True, color)
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += line_height
        pygame.display.flip()

    def cleanup(self) -> None:
        if self._enabled:
            self._stop_event.set()
            if self._pygame_thread and self._pygame_thread.is_alive():
                self._pygame_thread.join(timeout=2)
            pygame.quit()

    def enabled(self) -> bool:
        return self._enabled

    def display_text(self, message: str, color=(255, 255, 255)) -> None:
        if not self._enabled or not self.screen:
            return
        if not pygame.get_init():
            pygame.init()

        if not pygame.font.get_init():
            pygame.font.init()

        message_data = ScreenMessageDTO(message, color)

        try:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except queue.Empty:
                    break
            self._message_queue.put(message_data)
        except Exception as e:
            logger.error(f"{self.log_prefix} Error queueing message - {e}")

        self.screen.fill((0,0,0))
        font = pygame.font.SysFont("Arial", 36)
        text_surface = font.render(message, True, color)
        self.screen.blit(text_surface, (50, 150))
        pygame.display.flip()

    def get_current_message(self) -> str:
        return self._current_message
