from typing import Dict, Optional
from bop_common.enums.service_name import ServiceType

class ServiceRegistry:
    def __init__(self):
        self._services: Dict[ServiceType, object] = {}

    def register(self, service_type: ServiceType, instance: object) -> None:
        self._services[service_type] = instance

    def get(self, service_type: ServiceType) -> Optional[object]:
        return self._services.get(service_type)

SERVICE_REGISTRY = ServiceRegistry()
