from abc import ABC, abstractmethod
from typing import Any


class ScreenUpdaterInterface(ABC):
    @abstractmethod
    def update(self, data: Any) -> None:
        pass
