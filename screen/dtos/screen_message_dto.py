from dataclasses import dataclass
from typing import Tuple

@dataclass
class ScreenMessageDTO:
    message: str
    color: Tuple[int, int, int]