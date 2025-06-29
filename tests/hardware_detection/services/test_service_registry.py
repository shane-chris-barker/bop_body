from bop_common.enums.hardware_type import HardwareType
from hardware_detection.services.service_registry import SERVICE_STARTERS
from hardware_detection.services.screen_service_starter import ScreenServiceStarter

def test_screen_service_is_registered():
    assert HardwareType.SCREEN in SERVICE_STARTERS
    assert isinstance(SERVICE_STARTERS[HardwareType.SCREEN], ScreenServiceStarter)

def test_registry_only_contains_known_hardware_types():
    valid_keys = {HardwareType.SCREEN}
    for key in SERVICE_STARTERS:
        assert key in valid_keys, f"Unexpected key in registry: {key}"
