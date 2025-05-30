from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"

class LogSource(str, Enum):
    SERVICE = "service"
    CLIENT = "client"
    SYSTEM = "system"

class LogEntry(BaseModel):
    level: LogLevel
    message: str
    source: LogSource
    client_id: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class LogResponse(BaseModel):
    success: bool
    log_id: Optional[str] = None
    message: str 