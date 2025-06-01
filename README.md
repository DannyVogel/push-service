# Push Notification Service

This project is a FastAPI-based backend service for managing web push notification subscriptions, sending notifications to devices, and providing a robust logging system for both internal and external (client) events. It uses Supabase as a backend for storing subscriptions and logs, and supports secure access via API key or whitelisted origins.

## What It Does

- **Manages device subscriptions** for web push notifications
- **Sends notifications** to one or more devices using the [Web Push protocol](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- **Logs events and errors** from both the service and external clients, with filtering and statistics endpoints

## Access Control

All endpoints require either:

- A valid `x-api-key` header (see your admin for the API key), **or**
- Your request's `Origin` header to be whitelisted in the backend configuration

## Main Endpoints

All endpoints are prefixed with `/api` (except for logging, which uses `/logs`).

### 1. Subscribe a Device

- **POST** `/api/subscribe`
- **Body:**
  ```json
  {
    "subscription": {
      "endpoint": "...",
      "keys": { "p256dh": "...", "auth": "..." },
      "expiration_time": null,
      "metadata": {}
    },
    "device_id": "device-123"
  }
  ```
- **Purpose:** Register a device for push notifications.

### 2. Unsubscribe Devices

- **POST** `/api/unsubscribe`
- **Body:**
  ```json
  {
    "device_ids": ["device-123", "device-456"]
  }
  ```
- **Purpose:** Remove one or more devices from receiving notifications.

### 3. Send Notification

- **POST** `/api/notify`
- **Body:**
  ```json
  {
    "payload": {
      "title": "Hello!",
      "body": "This is a test notification.",
      "icon": "https://example.com/icon.png"
    },
    "device_ids": ["device-123"]
  }
  ```
- **Purpose:** Send a push notification to one or more devices.

### 4. Logging Endpoints

All logging endpoints are under `/logs` and require the same API key or whitelisted origin as above.

- **POST** `/logs/` — Create a log entry (see `LOGGING.md` for details)
- **GET** `/logs/` — Retrieve logs with optional filters
- **GET** `/logs/stats` — Get log statistics
- **POST** `/logs/error` — Quick error logging
- **POST** `/logs/info` — Quick info logging

## How to Call Endpoints

- **Headers:**
  - `Content-Type: application/json`
  - `x-api-key: <your-api-key>` (if not whitelisted)
- **Example with curl:**
  ```sh
  curl -X POST https://your-service.com/api/subscribe \
    -H "Content-Type: application/json" \
    -H "x-api-key: <your-api-key>" \
    -d '{ "subscription": { ... }, "device_id": "device-123" }'
  ```

## Environment & Setup

- Requires Python 3.8+
- Install dependencies: `pip install -r requirements.txt`
- Set up a `.env` file with your Supabase and VAPID credentials (see `app/config.py` for required variables)

---

For more details on logging, see [LOGGING.md](LOGGING.md).
