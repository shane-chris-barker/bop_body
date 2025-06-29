from bop_common.interfaces.service_starter_interface import ServiceStarterInterface
from bop_common.dtos.service_info_dto import ServiceInfoDTO
from bop_common.enums.service_name import ServiceType
from screen.screen_updater import ScreenUpdater

class ScreenServiceStarter(ServiceStarterInterface):

    def start(self) -> ServiceInfoDTO:
        screen_updater = ScreenUpdater()
        screen_updater.start()
        return ServiceInfoDTO(
            service=ServiceType.SCREEN,
            instance=screen_updater,
            cleanup_resource=screen_updater
        )
