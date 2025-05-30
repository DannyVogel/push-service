from fastapi import Request, HTTPException, Query
from typing import Optional, List
from datetime import datetime, timedelta
from app.models.log import LogEntry, LogResponse, LogLevel, LogSource
from app.utils.logger import logger
from app.dependencies import get_supabase_client
from app.utils.router import create_logger_router

router = create_logger_router()

@router.post("/", response_model=LogResponse)
async def create_log(log_entry: LogEntry, request: Request):
    """
    Create a new log entry. Can be used by the service itself or external clients.
    Automatically captures client information from the request.
    """
    try:
        # Extract client information from request
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Override with request data if not provided
        if not log_entry.ip_address:
            log_entry.ip_address = client_ip
        if not log_entry.user_agent:
            log_entry.user_agent = user_agent
        if not log_entry.timestamp:
            log_entry.timestamp = datetime.utcnow()
        
        # Log the entry
        log_id = await logger.log(
            level=log_entry.level,
            message=log_entry.message,
            source=log_entry.source,
            client_id=log_entry.client_id,
            user_agent=log_entry.user_agent,
            ip_address=log_entry.ip_address,
            metadata=log_entry.metadata
        )
        
        return LogResponse(
            success=True,
            log_id=log_id,
            message="Log entry created successfully"
        )
        
    except Exception as e:
        # Fallback logging to console if database fails
        await logger.error(f"Failed to create log entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create log entry")

@router.get("/", response_model=List[dict])
async def get_logs(
    level: Optional[LogLevel] = Query(None, description="Filter by log level"),
    source: Optional[LogSource] = Query(None, description="Filter by log source"),
    client_id: Optional[str] = Query(None, description="Filter by client ID"),
    hours: Optional[int] = Query(24, description="Get logs from last N hours"),
    limit: Optional[int] = Query(100, description="Maximum number of logs to return")
):
    """
    Retrieve logs with optional filtering. Useful for debugging and monitoring.
    """
    try:
        supabase = get_supabase_client()
        
        # Build query
        query = supabase.table("logs").select("*")
        
        # Apply filters
        if level:
            query = query.eq("level", level.value)
        if source:
            query = query.eq("source", source.value)
        if client_id:
            query = query.eq("client_id", client_id)
        
        # Time filter
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.gte("timestamp", cutoff_time.isoformat())
        
        # Execute query
        result = query.order("timestamp", desc=True).limit(limit).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        await logger.error(f"Failed to retrieve logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs")

@router.get("/stats")
async def get_log_stats():
    """
    Get logging statistics for monitoring and analytics.
    """
    try:
        supabase = get_supabase_client()
        
        # Get stats for the last 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Count by level
        level_stats = {}
        for level in LogLevel:
            result = supabase.table("logs").select("id", count="exact").eq("level", level.value).gte("timestamp", cutoff_time.isoformat()).execute()
            level_stats[level.value] = result.count if result.count else 0
        
        # Count by source
        source_stats = {}
        for source in LogSource:
            result = supabase.table("logs").select("id", count="exact").eq("source", source.value).gte("timestamp", cutoff_time.isoformat()).execute()
            source_stats[source.value] = result.count if result.count else 0
        
        # Total logs in last 24h
        total_result = supabase.table("logs").select("id", count="exact").gte("timestamp", cutoff_time.isoformat()).execute()
        total_logs = total_result.count if total_result.count else 0
        
        return {
            "period": "last_24_hours",
            "total_logs": total_logs,
            "by_level": level_stats,
            "by_source": source_stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        await logger.error(f"Failed to get log stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get log statistics")

# Convenience endpoints for different log levels
@router.post("/error")
async def log_error(message: str, request: Request, client_id: Optional[str] = None, metadata: Optional[dict] = None):
    """Quick endpoint for logging errors"""
    log_entry = LogEntry(
        level=LogLevel.ERROR,
        message=message,
        source=LogSource.CLIENT,
        client_id=client_id,
        metadata=metadata
    )
    return await create_log(log_entry, request)

@router.post("/info")
async def log_info(message: str, request: Request, client_id: Optional[str] = None, metadata: Optional[dict] = None):
    """Quick endpoint for logging info messages"""
    log_entry = LogEntry(
        level=LogLevel.INFO,
        message=message,
        source=LogSource.CLIENT,
        client_id=client_id,
        metadata=metadata
    )
    return await create_log(log_entry, request) 