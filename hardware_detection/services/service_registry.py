from bop_common.enums.hardware_type import HardwareType
from hardware_detection.services.screen_service_starter import ScreenServiceStarter
from bop_common.interfaces.service_starter_interface import ServiceStarterInterface

SERVICE_STARTERS: dict[HardwareType, ServiceStarterInterface] = {
    HardwareType.SCREEN: ScreenServiceStarter(),
}
