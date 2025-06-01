from dataclasses import dataclass
from typing import Optional

@dataclass
class NotificationResult:
    device_id: str
    success: bool
    error: Optional[str] = None 