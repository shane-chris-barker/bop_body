from abc import ABC, abstractmethod

class DeviceServiceInterface(ABC):

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

