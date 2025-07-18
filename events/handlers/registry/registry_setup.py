from bop_common.enums.event_type import EventType
from bop_common.enums.service_name import ServiceType
from events.handlers.angry_handler import AngryHandler
from events.handlers.dance_handler import DanceHandler
from events.handlers.happy_handler import HappyHandler
from events.handlers.love_handler import LoveHandler
from events.handlers.registry.handler_registry import HandlerRegistry
from events.handlers.sad_handler import SadHandler
from events.handlers.weather_report_handler import WeatherReportHandler
from hardware_detection.services.service_registry import SERVICE_REGISTRY
from screen.updaters.weather_report_screen_updater import WeatherReportScreenUpdater

def register_handlers() -> None:
    screen_starter = SERVICE_REGISTRY.get(ServiceType.SCREEN)
    if screen_starter and screen_starter.enabled:
        screen_updater = screen_starter.screen_updater
        weather_updater = WeatherReportScreenUpdater(screen_updater)
        HandlerRegistry.register(
            EventType.BOP_DANCE,
            lambda: DanceHandler(screen_updater)
        )
        HandlerRegistry.register(
            EventType.BOP_HAPPY,
            lambda: HappyHandler(screen_updater)
        )
        HandlerRegistry.register(
            EventType.BOP_LOVE,
            lambda: LoveHandler(screen_updater)
        )
        HandlerRegistry.register(
            EventType.BOP_ANGRY,
            lambda: AngryHandler(screen_updater)
        )
        HandlerRegistry.register(
            EventType.BOP_SAD,
            lambda: SadHandler(screen_updater)
        )
        HandlerRegistry.register(
            EventType.BOP_WEATHER_REPORT,
            lambda: WeatherReportHandler(weather_updater)
        )
