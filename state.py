from dataclasses import dataclass
from typing import Optional

@dataclass
class AppState:
    filename: Optional[str] = None
