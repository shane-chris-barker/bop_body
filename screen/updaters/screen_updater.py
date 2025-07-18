import logging
logger = logging.getLogger(__name__)
import pygame

class ScreenUpdater:
    def __init__(self) -> None:
        self.screen = None
        self.log_prefix = "[📺 SCREEN UPDATER]"
        self._current_color = (255, 255, 255)
        self._current_message = "Bop is putting his best face on!"

    def display_text(self, message: str, color=(255, 255, 255)) -> None:
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 36)
        lines = message.split('\n')
        y_offset = 150
        line_height = font.get_linesize()
        for line in lines:
            if line.strip():
                text_surface = font.render(line, True, color)
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += line_height
        pygame.display.flip()

    def get_current_message(self) -> str:
        return self._current_message

    def init_screen(self):
        self.screen = pygame.display.set_mode((800, 600))
