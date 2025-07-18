import os
from typing import Set
import logging
from bop_common.enums.hardware_type import HardwareType
from bop_common.dtos.hardware_config_dto import HardwareConfigDTO
logger = logging.getLogger(__name__)

class HardwareConfigService:
    screen_activated_key = "SCREEN_INSTALLED"
    def __init__(self):
        self.log_prefix = f"[🔧 {self.__class__.__name__}]"
        self._device_configs = {
            HardwareType.SCREEN: HardwareConfigDTO(
                device_type=HardwareType.SCREEN,
                enabled=self._get_env_bool(self.screen_activated_key, False),
                env_key=self.screen_activated_key
            )
        }
        self._log_configuration()

    @staticmethod
    def _get_env_bool(key: str, default: bool = False) -> bool:
        env_value = os.getenv(key)
        if env_value is None:
            return default
        return env_value.lower() in ('true', '1', 'yes', 'on')

    def _log_configuration(self) -> None:
        logger.info(f"{self.log_prefix} Device Configuration:")
        for device_type, config in self._device_configs.items():
            status = "Enabled" if config.enabled else "Disabled"
            logger.info(f"{self.log_prefix} {device_type.value.upper()} IS {status}")

    def is_device_enabled_in_config(self, device_type: HardwareType) -> bool:
        config = self._device_configs.get(device_type)
        return config.enabled if config else False

    def get_config_enabled_devices(self) -> Set[HardwareType]:
        return {
            device_type for device_type, config in self._device_configs.items()
            if config.enabled
        }
