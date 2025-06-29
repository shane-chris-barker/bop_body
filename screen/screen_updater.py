from hardware_detection.services.device_service_interface import DeviceServiceInterface
class ScreenUpdater(DeviceServiceInterface):
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = enabled

    def start(self) -> None:
        return

    def cleanup(self) -> None:
        return

    def enabled(self) -> bool:
        return self._enabled
