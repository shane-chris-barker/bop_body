import pytest
from unittest.mock import patch
import os
from hardware_detection.services.hardware_config_service import HardwareConfigService
from bop_common.enums.hardware_type import HardwareType

class TestHardwareConfigService:
    screen_installed_key = "SCREEN_INSTALLED"

    @pytest.fixture(autouse=True)
    def clear_env(self, monkeypatch):
        monkeypatch.delenv(self.screen_installed_key, raising=False)

    def test_default_env_vars_disabled(self):
        service = HardwareConfigService()
        assert not service.is_device_enabled_in_config(HardwareType.SCREEN)
        assert service.get_config_enabled_devices() == set()

    @pytest.mark.parametrize("screen_value", ["true", "1", "yes", "on","TRUE"])
    def test_enabled_var(self, screen_value, monkeypatch):
        monkeypatch.setenv(self.screen_installed_key, screen_value)
        service = HardwareConfigService()
        assert service.is_device_enabled_in_config(HardwareType.SCREEN)
        assert HardwareType.SCREEN in service.get_config_enabled_devices()

    @pytest.mark.parametrize("screen_value", ["false", "0", "no", "off","FALSE"])
    def test_disabled_var(self, screen_value):
        test_env = {
            "SCREEN_INSTALLED": screen_value
        }
        with patch.dict(os.environ, test_env, clear=False):
            service = HardwareConfigService()
            assert not service.is_device_enabled_in_config(HardwareType.SCREEN)
            assert HardwareType.SCREEN not in service.get_config_enabled_devices()
