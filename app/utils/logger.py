import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from app.dependencies import get_supabase_client
from app.models.log import LogLevel, LogSource, LogEntry

class StructuredLogger:
    def __init__(self):
        # Set up console logger
        self.console_logger = logging.getLogger("push_service")
        self.console_logger.setLevel(logging.DEBUG)
        
        # Create console handler with structured JSON format
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # JSON formatter for structured logging
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": record.levelname.lower(),
                    "message": record.getMessage(),
                    "source": "service",
                    "logger": record.name,
                }
                
                # Add extra fields if they exist
                if hasattr(record, 'client_id'):
                    log_data["client_id"] = record.client_id
                if hasattr(record, 'metadata'):
                    log_data["metadata"] = record.metadata
                if hasattr(record, 'ip_address'):
                    log_data["ip_address"] = record.ip_address
                if hasattr(record, 'user_agent'):
                    log_data["user_agent"] = record.user_agent
                    
                return json.dumps(log_data)
        
        console_handler.setFormatter(JSONFormatter())
        self.console_logger.addHandler(console_handler)
    
    async def log(self, 
                  level: LogLevel, 
                  message: str, 
                  source: LogSource = LogSource.SERVICE,
                  client_id: Optional[str] = None,
                  user_agent: Optional[str] = None,
                  ip_address: Optional[str] = None,
                  metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Log a message to both console and database
        Returns the log ID if database logging succeeds
        """
        
        # Always log to console
        log_data = {
            "client_id": client_id,
            "metadata": metadata,
            "ip_address": ip_address,
            "user_agent": user_agent
        }
        
        # Map LogLevel to logging levels
        level_map = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARN: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL
        }
        
        self.console_logger.log(level_map[level], message, extra=log_data)
        
        # Try to log to database using centralized client
        try:
            supabase = get_supabase_client()
            log_entry = {
                "level": level.value,
                "message": message,
                "source": source.value,
                "client_id": client_id,
                "user_agent": user_agent,
                "ip_address": ip_address,
                "metadata": metadata,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            result = supabase.table("logs").insert(log_entry).execute()
            if result.data:
                log_id = result.data[0].get("id")
                if log_id:
                    print(f"New {level.value} logged with id: {log_id}")
                return log_id
        except Exception as e:
            self.console_logger.error(f"Failed to log to database: {e}")
        
        return None
    
    # Convenience methods
    async def debug(self, message: str, **kwargs):
        return await self.log(LogLevel.DEBUG, message, **kwargs)
    
    async def info(self, message: str, **kwargs):
        return await self.log(LogLevel.INFO, message, **kwargs)
    
    async def warn(self, message: str, **kwargs):
        return await self.log(LogLevel.WARN, message, **kwargs)
    
    async def error(self, message: str, **kwargs):
        return await self.log(LogLevel.ERROR, message, **kwargs)
    
    async def critical(self, message: str, **kwargs):
        return await self.log(LogLevel.CRITICAL, message, **kwargs)

# Global logger instance
logger = StructuredLogger() 