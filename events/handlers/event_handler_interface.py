from bop_common.dtos.event_dto import EventDTO

class EventHandlerInterface:
    def handle(self, dto: EventDTO) -> None:
        pass