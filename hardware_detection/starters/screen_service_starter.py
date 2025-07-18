import logging
from hardware_detection.services.device_service_interface import DeviceServiceInterface
logger = logging.getLogger(__name__)
import threading
import queue
import pygame
from bop_common.interfaces.service_starter_interface import ServiceStarterInterface
from bop_common.dtos.service_info_dto import ServiceInfoDTO
from bop_common.enums.service_name import ServiceType
from screen.updaters.screen_updater import ScreenUpdater

class ScreenServiceStarter(ServiceStarterInterface, DeviceServiceInterface):
    def __init__(self, enabled: bool = True):
        self._enabled = enabled
        self._stop_event = threading.Event()
        self._thread = None
        self.screen_updater = ScreenUpdater()
        self.log_prefix = "[📺 SCREEN STARTER]"
        self._message_queue = queue.Queue()

    def _run_pygame_loop(self) -> None:
        try:
            pygame.init()
            self.screen_updater.init_screen()
            clock = pygame.time.Clock()
            while not self._stop_event.is_set():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        logger.info(f"{self.log_prefix} Bop's face is shutting down")
                        self._stop_event.set()
                        break
                    try:
                        message_data = self._message_queue.get_nowait()
                        self.screen_updater.display_text(message_data.message, message_data.color)
                    except queue.Empty:
                        pass
                clock.tick(30)
            pygame.quit()
            logger.info(f"{self.log_prefix} Bop's face is shutting down")
        except Exception as e:
            logger.error(f"{self.log_prefix} Error in pygame - {e}")
            if 'pygame' in locals():
                pygame.quit()

    def start(self) -> ServiceInfoDTO:
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_pygame_loop, daemon=True)
        self._thread.start()
        return ServiceInfoDTO(
            service=ServiceType.SCREEN,
            instance=self,
            cleanup_resource=self
        )

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join()

    def cleanup(self) -> None:
        if self._enabled:
            self._stop_event.set()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=2)
            pygame.quit()

    def enabled(self) -> bool:
        return self._enabled
