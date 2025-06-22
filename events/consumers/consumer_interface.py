from abc import ABC, abstractmethod
from bop_common.dtos.event_dto import EventDTO

class ConsumerInterface(ABC):
    @abstractmethod
    def consume(self, message: EventDTO) -> None:
        pass
