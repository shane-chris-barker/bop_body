import unittest
from unittest.mock import MagicMock
from screen.updaters.weather_report_screen_updater import WeatherReportScreenUpdater
from screen.updaters.screen_updater import ScreenUpdater
from bop_common.dtos.weather.weather_data_dto import WeatherDataDTO
from bop_common.dtos.weather.daily_forecast_dto import DailyForecastDTO

class TestWeatherReportScreenUpdater(unittest.TestCase):
    def setUp(self):
        self.mock_core = MagicMock(spec=ScreenUpdater)
        self.updater = WeatherReportScreenUpdater(self.mock_core)
        self.weather = WeatherDataDTO(
            city="Narnia",
            forecast=[
                DailyForecastDTO("2025‑07‑18", 28.6, "Overcast"),
                DailyForecastDTO("2025‑07‑19", 24.3, "Thunderstorm with slight hail"),
                DailyForecastDTO("2025‑07‑20", 22.1, "Slight rain"),
                DailyForecastDTO("2025‑07‑21", 21.4, "Overcast"),
                DailyForecastDTO("2025‑07‑22", 22.7, "Slight rain"),
                DailyForecastDTO("2025‑07‑23", 22.0, "Overcast"),
                DailyForecastDTO("2025‑07‑24", 23.6, "Overcast"),
            ]
        )

    def test_update_sends_formatted_message(self):
        self.updater.update(self.weather)
        self.mock_core.display_text.assert_called_once()
        sent_message, sent_kwargs = self.mock_core.display_text.call_args
        message_text = sent_message[0]
        colour = sent_kwargs.get("color")
        self.assertIn("Weather forcast for Narnia:", message_text)
        self.assertIn("Today - 2025‑07‑18 - 28.6°C", message_text)
        self.assertIn("Thunderstorm with slight hail", message_text)
        self.assertTrue(message_text.count("\n") >= 6)
        self.assertEqual(colour, (255, 255, 255))
