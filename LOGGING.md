# Logging System Documentation

## Overview

This push service includes a comprehensive logging system that supports both console and database logging. It's designed to handle logs from:

- **The service itself** (internal operations, errors, notifications)
- **External frontend clients** (JavaScript errors, user actions, etc.)

## Features

✅ **Dual Logging**: Console + Database  
✅ **Structured JSON Logs**: Easy parsing and filtering  
✅ **Client Information**: Automatic IP, User-Agent capture  
✅ **Metadata Support**: Custom JSON data per log  
✅ **Log Analytics**: Statistics and filtering endpoints  
✅ **Multiple Log Levels**: DEBUG, INFO, WARN, ERROR, CRITICAL

## API Endpoints

### 1. Create Log Entry

```http
POST /logs/
Content-Type: application/json

{
  "level": "error",
  "message": "User authentication failed",
  "source": "client",
  "client_id": "user123",
  "metadata": {
    "page": "/login",
    "errorCode": "AUTH_001"
  }
}
```

### 2. Quick Error Logging

```http
POST /logs/error?message=Something went wrong&client_id=user123
```

### 3. Quick Info Logging

```http
POST /logs/info?message=User logged in&client_id=user123
```

### 4. Get Logs with Filters

```http
GET /logs/?level=error&hours=24&limit=50
GET /logs/?source=client&client_id=user123
```

### 5. Get Log Statistics

```http
GET /logs/stats
```

## Frontend JavaScript Usage

### Basic Error Logging

```javascript
// Log JavaScript errors to your service
async function logError(message, metadata = {}) {
  try {
    await fetch("https://your-push-service.com/logs/error", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        client_id: getUserId(), // Your user ID function
        metadata,
      }),
    });
  } catch (err) {
    console.error("Failed to log error:", err);
  }
}

// Catch all unhandled errors
window.addEventListener("error", (event) => {
  logError(`JavaScript Error: ${event.error.message}`, {
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    stack: event.error.stack,
  });
});

// Catch unhandled promise rejections
window.addEventListener("unhandledrejection", (event) => {
  logError(`Unhandled Promise Rejection: ${event.reason}`, {
    type: "unhandledrejection",
  });
});
```

### User Action Logging

```javascript
// Log user interactions
function logUserAction(action, details = {}) {
  fetch("https://your-push-service.com/logs/info", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: `User action: ${action}`,
      client_id: getUserId(),
      metadata: {
        action,
        timestamp: new Date().toISOString(),
        ...details,
      },
    }),
  }).catch(console.error);
}

// Usage examples
document.getElementById("subscribe-btn").addEventListener("click", () => {
  logUserAction("subscribe_clicked", {
    button_id: "subscribe-btn",
    page: window.location.pathname,
  });
});
```

### API Error Logging

```javascript
// Log API call failures
async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      logError(`API Error: ${response.status} ${response.statusText}`, {
        url,
        status: response.status,
        method: options.method || "GET",
      });
    }
    return response;
  } catch (error) {
    logError(`Network Error: ${error.message}`, {
      url,
      error_type: "network_error",
    });
    throw error;
  }
}
```

## Service Internal Usage

### In Your FastAPI Routes

```python
from app.utils.logger import logger
from app.models.log import LogSource

@router.post("/some-endpoint")
async def some_endpoint(data: SomeModel):
    try:
        # Log info
        await logger.info(
            "Processing request",
            source=LogSource.SERVICE,
            metadata={"endpoint": "/some-endpoint", "data_size": len(str(data))}
        )

        # Your business logic here
        result = process_data(data)

        # Log success
        await logger.info(
            "Request processed successfully",
            source=LogSource.SERVICE,
            metadata={"result_size": len(str(result))}
        )

        return result

    except Exception as e:
        # Log error with context
        await logger.error(
            f"Failed to process request: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "endpoint": "/some-endpoint",
                "input_data": str(data)[:500]  # Truncate for safety
            }
        )
        raise HTTPException(status_code=500, detail="Processing failed")
```

### Startup/Background Task Logging

```python
from app.utils.logger import logger

@app.on_event("startup")
async def startup_event():
    await logger.info("Service starting up", source=LogSource.SYSTEM)

async def background_task():
    try:
        # Task logic
        await logger.debug("Background task completed", source=LogSource.SYSTEM)
    except Exception as e:
        await logger.error(f"Background task failed: {e}", source=LogSource.SYSTEM)
```

## Log Levels Guide

- **DEBUG**: Detailed development info (not shown in production)
- **INFO**: General operational messages (user actions, successful operations)
- **WARN**: Something unexpected but not breaking (deprecated API usage)
- **ERROR**: Error conditions that need attention (failed API calls, user errors)
- **CRITICAL**: Serious errors requiring immediate action (service failures)

## Monitoring and Analytics

### View Recent Errors

```bash
curl "https://your-service.com/logs/?level=error&hours=1"
```

### Monitor Specific Client

```bash
curl "https://your-service.com/logs/?client_id=user123&hours=24"
```

### Get Daily Statistics

```bash
curl "https://your-service.com/logs/stats"
```

### Example Statistics Response

```json
{
  "period": "last_24_hours",
  "total_logs": 1250,
  "by_level": {
    "debug": 500,
    "info": 600,
    "warn": 100,
    "error": 45,
    "critical": 5
  },
  "by_source": {
    "service": 800,
    "client": 400,
    "system": 50
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Console vs Database Logging

| Feature         | Console            | Database        |
| --------------- | ------------------ | --------------- |
| **Development** | ✅ Perfect         | ⚠️ Optional     |
| **Production**  | ⚠️ Limited         | ✅ Essential    |
| **Persistence** | ❌ Lost on restart | ✅ Permanent    |
| **Filtering**   | ❌ Basic           | ✅ Advanced     |
| **Analytics**   | ❌ None            | ✅ Full         |
| **Performance** | ✅ Fast            | ⚠️ Network call |

## Best Practices

1. **Use appropriate log levels** - Don't log everything as ERROR
2. **Include context** - Add metadata for debugging
3. **Log user actions** - Track feature usage and errors
4. **Monitor critical paths** - Log authentication, payments, etc.
5. **Rate limit client logging** - Prevent spam
6. **Sanitize sensitive data** - Don't log passwords, tokens
7. **Use structured logging** - JSON format for better parsing

## Environment Configuration

Make sure these environment variables are set:

```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## Troubleshooting

### Logs not appearing in database?

1. Check Supabase connection
2. Verify table exists (`logs`)
3. Check service role permissions
4. Console logs should still work

### Too many logs?

1. Adjust log levels in production
2. Add rate limiting for client logs
3. Set up log rotation/cleanup

### Performance concerns?

1. Logs are async by default
2. Console logging continues if DB fails
3. Consider batching for high-volume scenarios
