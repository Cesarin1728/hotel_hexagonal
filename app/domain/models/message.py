from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Message:
    id: Optional[int]
    user: str
    content: str
    created_at: datetime