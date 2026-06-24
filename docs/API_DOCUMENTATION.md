# CrisisGuardian AI - API Documentation

## Overview

CrisisGuardian AI provides a comprehensive REST API for disaster response and emergency management. All endpoints are built with FastAPI and support JSON request/response formats.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API uses no authentication. For production, implement OAuth2 or API key authentication.

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "CrisisGuardian AI"
}
```

---

### 2. Analyze Disaster

**Endpoint:** `POST /analyze`

**Description:** Analyzes a disaster-related query using the multi-agent workflow.

**Request Body:**
```json
{
  "user_id": "user123",
  "message": "There's heavy flooding in my area",
  "location": "Mumbai, India",
  "crisis_type": "flood"
}
```

**Response:**
```json
{
  "threat_level": "High",
  "risk_score": 7,
  "risk_reason": "Heavy rainfall triggering flood watches...",
  "verification_status": "Verified via official bulletins",
  "weather_summary": "Heavy Rain, 28.5°C, Wind: 45.6 km/h",
  "guidance": "**CRITICAL EMERGENCY DIRECTIVE**...",
  "checklist": ["Water", "First Aid Kit", "Power Bank", "Flashlight"],
  "recommended_actions": ["Evacuate low-lying sectors", "Seek concrete shelter"],
  "monitoring_data": {
    "Coordinator Agent": {"status": "Completed", "exec_time": "150 ms"},
    "Weather Agent": {"status": "Completed", "exec_time": "200 ms"}
  }
}
```

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `500 Internal Server Error` - Processing error

---

### 3. Find Resources

**Endpoint:** `POST /resources`

**Description:** Locates nearby emergency resources (shelters, hospitals, police, fire stations).

**Request Body:**
```json
{
  "location": "Mumbai, India"
}
```

**Response:**
```json
{
  "hospitals": [
    {
      "name": "Mumbai General Emergency Hospital",
      "address": "100 Recovery Road",
      "distance_miles": 1.2,
      "status": "Active (High Traffic)"
    }
  ],
  "shelters": [
    {
      "name": "Community Safe House",
      "address": "402 Safe Haven Ave",
      "distance_miles": 0.8,
      "capacity": "300 / 500 occupied",
      "status": "Open"
    }
  ],
  "police_stations": [...],
  "fire_stations": [...]
}
```

---

### 4. Upload Document for Analysis

**Endpoint:** `POST /document-analysis`

**Description:** Uploads a PDF emergency document and performs RAG-based analysis.

**Request:** Multipart form data with PDF file

**Response:**
```json
{
  "summary": "The document describes regional emergency guidelines...",
  "warnings": [
    "Evacuate when water rises above level tier 3 (2.5 meters)",
    "Ensure utilities are switched off before departing"
  ],
  "recommendations": [
    "Prepare a minimum 72-hour emergency go-bag",
    "Review local evacuation routes"
  ]
}
```

---

### 5. Query Uploaded Document

**Endpoint:** `POST /document-query`

**Description:** Ask questions about a previously uploaded emergency document.

**Request Body:**
```json
{
  "query": "What should I do if flooding occurs?"
}
```

**Response:**
```json
{
  "answer": "According to the document matching sections: ... residents should evacuate to designated safe zones immediately ..."
}
```

---

### 6. Create SOS Alert

**Endpoint:** `POST /api/sos`

**Description:** Triggers an emergency SOS dispatch alert.

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+91-9876543210",
  "location": "Mumbai, Maharashtra",
  "description": "Trapped on rooftop, water rising rapidly"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Emergency SOS successfully recorded.",
  "dispatch_confirmation": {
    "status": "Dispatched",
    "eta": "12-15 minutes",
    "unit": "Local Emergency Response Unit & Rescue Team",
    "ref_number": "SOS-1719230400"
  }
}
```

---

### 7. System Status

**Endpoint:** `GET /system-status`

**Description:** Returns the operational status of all system components.

**Response:**
```json
{
  "backend": "online",
  "workflow": "active",
  "mcp": "connected"
}
```

---

### 8. Agent Status

**Endpoint:** `GET /agent-status`

**Description:** Returns the status of individual AI agents.

**Response:**
```json
{
  "coordinator_agent": "active",
  "weather_agent": "active",
  "news_agent": "active",
  "resource_agent": "active",
  "risk_agent": "active",
  "response_agent": "active"
}
```

---

## Error Handling

All errors return appropriate HTTP status codes with detailed messages:

```json
{
  "detail": "Only PDF documents are supported."
}
```

**Common Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Server-side error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, implement rate limiting (e.g., 100 requests/minute).

---

## CORS Configuration

By default, CORS is enabled for all origins. Configure in `.env`:

```
API_CORS_ORIGINS=["http://localhost:8501", "http://localhost:3000"]
```

---

## Examples

### Using cURL

```bash
# Health check
curl -X GET http://localhost:8000/health

# Analyze disaster
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Heavy flooding in my area",
    "location": "Mumbai",
    "crisis_type": "flood"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "user_id": "user123",
        "message": "Earthquake happening!",
        "location": "Tokyo",
        "crisis_type": "earthquake"
    }
)

print(response.json())
```

---

## Future Enhancements

- WebSocket support for real-time updates
- Batch processing endpoints
- Advanced authentication (OAuth2, JWT)
- API versioning (v1, v2, etc.)
- Webhook integrations
