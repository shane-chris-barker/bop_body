import logging
from bop_common.dtos.weather.weather_data_dto import WeatherDataDTO
from screen.screen_updater import ScreenUpdater
logger = logging.getLogger(__name__)
from bop_common.dtos.event_dto import EventDTO
from events.handlers.event_handler_interface import EventHandlerInterface

class WeatherReportHandler(EventHandlerInterface):
    def __init__(self, screen_updater: ScreenUpdater):
        self.log_prefix = "[🌡️ WEATHER REPORT HANDLER]"
        self.screen_updater = screen_updater

    # TODO - Refactor this and the screen updater so we can move display and screen
    # based operations into it.
    def handle(self, dto: EventDTO):
        logger.info(f"{self.log_prefix} Bop is trying to forecast the weather!")
        try:
            weather_dto = WeatherDataDTO.from_dict(dto.payload)
            today = weather_dto.forecast[0]
            lines = [
                f"Weather forcast for {weather_dto.city}:",
                f"Today - {today.date} - {today.temperature}°C",
                f"{today.description}",
                ""
            ]

            for day in weather_dto.forecast[1:7]:
                lines.append(f"{day.date} - {day.temperature}°C - {day.description}")
            message = "\n".join(lines)
            self.screen_updater.display_text(message)

        except Exception as e:
            logger.warning(f"{self.log_prefix} Bop is unable to display weather report due to {e}")