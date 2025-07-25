from hardware_detection.starters.service_starters import SERVICE_STARTERS
from hardware_detection.services.service_registry import SERVICE_REGISTRY
from hardware_detection.services.hardware_config_service import HardwareConfigService
from bop_common.dtos.service_info_dto import ServiceInfoDTO
import logging

logger = logging.getLogger(__name__)

def start_enabled_services() -> list[ServiceInfoDTO]:
    log_prefix = "[🤖 MAIN]"
    device_config_service = HardwareConfigService()
    services: list[ServiceInfoDTO] = []
    enabled_devices = device_config_service.get_config_enabled_devices()
    for device_type in enabled_devices:
        logger.info(f"{log_prefix} Bop body config says we have a {device_type.name} enabled!")
        logger.info(f"{log_prefix} Bop body is trying to start services for the {device_type.name}")
        starter = SERVICE_STARTERS.get(device_type)
        if starter:
            try:
                service_info = starter.start()
                services.append(service_info)
                SERVICE_REGISTRY.register(service_info.service, service_info.instance)
                logger.info(f"{log_prefix} Bop body started the {service_info.service.name} service!")
            except Exception as e:
                logger.error(f"{log_prefix} Bop body couldn't start a device - {device_type.name} system: {e}")
    return services