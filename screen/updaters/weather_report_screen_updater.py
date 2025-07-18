from bop_common.dtos.weather.weather_data_dto import WeatherDataDTO
from screen.updaters.screen_updater import ScreenUpdater
from screen.updaters.screen_updater_interface import ScreenUpdaterInterface

class WeatherReportScreenUpdater(ScreenUpdaterInterface):
    def __init__(self, core: ScreenUpdater) -> None:
        self.core = core

    def update(self, weather_data: WeatherDataDTO) -> None:
        today = weather_data.forecast[0]
        lines = [
            f"Weather forcast for {weather_data.city}:",
            f"Today - {today.date} - {today.temperature}°C",
            f"{today.description}",
            ""
        ]

        for day in weather_data.forecast[1:7]:
            lines.append(f"{day.date} - {day.temperature}°C - {day.description}")
        message = "\n".join(lines)
        self.core.display_text(message, color=(255, 255, 255))
