from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class AppState:
    filename: Optional[str] = None
    recent_files: List[str] = field(default_factory=list)
    font_size: int = 12
