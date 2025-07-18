import logging
from bop_common.dtos.weather.weather_data_dto import WeatherDataDTO
from screen.updaters.weather_report_screen_updater import WeatherReportScreenUpdater
logger = logging.getLogger(__name__)
from bop_common.dtos.event_dto import EventDTO
from events.handlers.event_handler_interface import EventHandlerInterface

class WeatherReportHandler(EventHandlerInterface):
    def __init__(self, screen_updater: WeatherReportScreenUpdater):
        self.log_prefix = "[🌡️ WEATHER REPORT HANDLER]"
        self.screen_updater = screen_updater

    def handle(self, dto: EventDTO):
        logger.info(f"{self.log_prefix} Bop is trying to forecast the weather!")
        try:
            weather_dto = WeatherDataDTO.from_dict(dto.payload)
            self.screen_updater.update(weather_dto)
        except Exception as e:
            logger.warning(f"{self.log_prefix} Bop is unable to display weather report due to {e}")
