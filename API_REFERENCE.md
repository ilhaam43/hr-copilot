# HR Chatbot API Reference

## Daftar Isi
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL & Headers](#base-url--headers)
4. [Rate Limiting](#rate-limiting)
5. [Chatbot API](#chatbot-api)
6. [Employee API](#employee-api)
7. [Analytics API](#analytics-api)
8. [Health Check API](#health-check-api)
9. [Error Handling](#error-handling)
10. [SDK & Examples](#sdk--examples)

---

## Overview

HR Chatbot API menyediakan RESTful endpoints untuk mengintegrasikan sistem chatbot dengan aplikasi eksternal. API ini mendukung berbagai operasi seperti chat processing, employee data retrieval, dan analytics.

### API Features
- **Multi-language Support**: Indonesian dan English
- **AI-Powered Responses**: Menggunakan Ollama LLM
- **Intent Recognition**: Automatic intent classification
- **Context Awareness**: Maintains conversation context
- **Real-time Processing**: Fast response times
- **Comprehensive Analytics**: Detailed usage statistics

### Supported Formats
- **Request**: JSON
- **Response**: JSON
- **Encoding**: UTF-8

---

## Authentication

### API Key Authentication
```http
Authorization: Bearer YOUR_API_KEY
```

### Obtaining API Key
1. Login ke admin panel: `/admin/`
2. Navigate ke **API Keys** section
3. Generate new API key
4. Copy dan simpan API key dengan aman

### Token-based Authentication (Alternative)
```http
Authorization: Token YOUR_TOKEN
```

### Session Authentication (Web Interface)
```http
Cookie: sessionid=YOUR_SESSION_ID; csrftoken=YOUR_CSRF_TOKEN
X-CSRFToken: YOUR_CSRF_TOKEN
```

---

## Base URL & Headers

### Base URL
```
Production: https://your-domain.com/api/v1/
Development: http://localhost:8000/api/v1/
```

### Required Headers
```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer YOUR_API_KEY
User-Agent: YourApp/1.0
```

### Optional Headers
```http
X-Request-ID: unique-request-identifier
X-Client-Version: 1.0.0
Accept-Language: id-ID,en-US
```

---

## Rate Limiting

### Limits
- **Standard**: 100 requests per minute
- **Premium**: 1000 requests per minute
- **Enterprise**: Custom limits

### Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

---

## Chatbot API

### Send Message
Process user message dan dapatkan chatbot response.

**Endpoint**: `POST /chat/message/`

**Request Body**:
```json
{
  "message": "Berapa sisa cuti saya?",
  "user_id": "employee_123",
  "session_id": "session_abc123",
  "context": {
    "department": "IT",
    "role": "employee",
    "language": "id"
  },
  "metadata": {
    "source": "web_app",
    "timestamp": "2025-01-20T10:30:00Z"
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "response": "Sisa cuti Anda adalah 12 hari dari total 24 hari per tahun.",
    "intent": "leave_balance",
    "confidence": 0.95,
    "entities": [
      {
        "type": "leave_type",
        "value": "annual_leave",
        "confidence": 0.9
      }
    ],
    "suggestions": [
      "Bagaimana cara mengajukan cuti?",
      "Kapan periode cuti refresh?"
    ],
    "session_id": "session_abc123",
    "message_id": "msg_xyz789"
  },
  "processing_time": 0.45,
  "timestamp": "2025-01-20T10:30:01Z"
}
```

### Get Conversation History
Retrieve chat history untuk specific session.

**Endpoint**: `GET /chat/history/{session_id}/`

**Query Parameters**:
- `limit`: Number of messages (default: 50, max: 200)
- `offset`: Pagination offset (default: 0)
- `start_date`: Filter from date (ISO 8601)
- `end_date`: Filter to date (ISO 8601)

**Response**:
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": "msg_001",
        "message": "Halo, ada yang bisa saya bantu?",
        "response": "Halo! Saya siap membantu Anda dengan pertanyaan HR.",
        "intent": "greeting",
        "timestamp": "2025-01-20T10:25:00Z",
        "user_id": "employee_123"
      }
    ],
    "total_count": 15,
    "has_more": true
  }
}
```

### Clear Session
Clear conversation context untuk specific session.

**Endpoint**: `DELETE /chat/session/{session_id}/`

**Response**:
```json
{
  "success": true,
  "message": "Session cleared successfully"
}
```

---

## Employee API

### Get Employee Info
Retrieve employee information.

**Endpoint**: `GET /employees/{employee_id}/`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "employee_123",
    "name": "John Doe",
    "email": "john.doe@company.com",
    "department": "IT",
    "position": "Software Developer",
    "hire_date": "2023-01-15",
    "leave_balance": {
      "annual_leave": 12,
      "sick_leave": 8,
      "personal_leave": 3
    },
    "manager": {
      "id": "manager_456",
      "name": "Jane Smith"
    }
  }
}
```

### Search Employees
Search employees dengan various filters.

**Endpoint**: `GET /employees/search/`

**Query Parameters**:
- `q`: Search query
- `department`: Filter by department
- `position`: Filter by position
- `status`: active, inactive, all (default: active)
- `limit`: Results limit (default: 20, max: 100)
- `offset`: Pagination offset

**Response**:
```json
{
  "success": true,
  "data": {
    "employees": [
      {
        "id": "employee_123",
        "name": "John Doe",
        "department": "IT",
        "position": "Software Developer",
        "status": "active"
      }
    ],
    "total_count": 45,
    "has_more": true
  }
}
```

---

## Analytics API

### Chat Analytics
Get chatbot usage analytics.

**Endpoint**: `GET /analytics/chat/`

**Query Parameters**:
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)
- `granularity`: hour, day, week, month (default: day)
- `department`: Filter by department
- `intent`: Filter by intent type

**Response**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_messages": 1250,
      "unique_users": 89,
      "avg_response_time": 0.65,
      "satisfaction_score": 4.2
    },
    "time_series": [
      {
        "date": "2025-01-20",
        "messages": 45,
        "users": 12,
        "avg_response_time": 0.58
      }
    ],
    "top_intents": [
      {
        "intent": "leave_balance",
        "count": 234,
        "percentage": 18.7
      }
    ],
    "user_satisfaction": {
      "very_satisfied": 45,
      "satisfied": 32,
      "neutral": 15,
      "dissatisfied": 6,
      "very_dissatisfied": 2
    }
  }
}
```

### Intent Analytics
Analyze intent recognition performance.

**Endpoint**: `GET /analytics/intents/`

**Response**:
```json
{
  "success": true,
  "data": {
    "intents": [
      {
        "name": "leave_balance",
        "total_requests": 234,
        "avg_confidence": 0.92,
        "success_rate": 0.95,
        "avg_response_time": 0.45
      }
    ],
    "overall_stats": {
      "total_intents": 12,
      "avg_confidence": 0.87,
      "overall_success_rate": 0.91
    }
  }
}
```

---

## Health Check API

### System Health
Check overall system health.

**Endpoint**: `GET /health/`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time": 0.05
    },
    "ollama": {
      "status": "healthy",
      "response_time": 0.12,
      "models": ["llama3.2:3b", "nomic-embed-text"]
    },
    "cache": {
      "status": "healthy",
      "hit_rate": 0.85
    }
  },
  "metrics": {
    "uptime": 86400,
    "memory_usage": 0.65,
    "cpu_usage": 0.23,
    "disk_usage": 0.45
  }
}
```

### Service Status
Check specific service status.

**Endpoint**: `GET /health/{service}/`

Available services: `database`, `ollama`, `cache`, `storage`

**Response**:
```json
{
  "service": "ollama",
  "status": "healthy",
  "details": {
    "url": "http://localhost:11434",
    "models": ["llama3.2:3b", "nomic-embed-text"],
    "response_time": 0.12,
    "last_check": "2025-01-20T10:30:00Z"
  }
}
```

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Specific field error"
    },
    "request_id": "req_123456789"
  },
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request format atau parameter tidak valid |
| `UNAUTHORIZED` | 401 | API key tidak valid atau missing |
| `FORBIDDEN` | 403 | Tidak memiliki permission untuk resource |
| `NOT_FOUND` | 404 | Resource tidak ditemukan |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit terlampaui |
| `INTERNAL_ERROR` | 500 | Server internal error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `OLLAMA_ERROR` | 502 | Ollama service error |
| `DATABASE_ERROR` | 503 | Database connection error |

### Validation Errors
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "message": ["This field is required"],
      "user_id": ["Invalid user ID format"]
    }
  }
}
```

---

## SDK & Examples

### Python SDK

#### Installation
```bash
pip install hrbot-api-client
```

#### Basic Usage
```python
from hrbot_api import HRBotClient

# Initialize client
client = HRBotClient(
    base_url="https://your-domain.com/api/v1/",
    api_key="your-api-key"
)

# Send message
response = client.chat.send_message(
    message="Berapa sisa cuti saya?",
    user_id="employee_123",
    session_id="session_abc"
)

print(f"Response: {response.data.response}")
print(f"Intent: {response.data.intent}")
print(f"Confidence: {response.data.confidence}")

# Get employee info
employee = client.employees.get("employee_123")
print(f"Employee: {employee.data.name}")
print(f"Department: {employee.data.department}")

# Get analytics
analytics = client.analytics.chat(
    start_date="2025-01-01",
    end_date="2025-01-31"
)
print(f"Total messages: {analytics.data.summary.total_messages}")
```

#### Error Handling
```python
from hrbot_api import HRBotClient, HRBotError

try:
    response = client.chat.send_message(
        message="Hello",
        user_id="invalid_user"
    )
except HRBotError as e:
    print(f"Error: {e.code} - {e.message}")
    if e.details:
        print(f"Details: {e.details}")
```

### JavaScript SDK

#### Installation
```bash
npm install hrbot-api-client
```

#### Basic Usage
```javascript
import { HRBotClient } from 'hrbot-api-client';

// Initialize client
const client = new HRBotClient({
  baseUrl: 'https://your-domain.com/api/v1/',
  apiKey: 'your-api-key'
});

// Send message
try {
  const response = await client.chat.sendMessage({
    message: 'Berapa sisa cuti saya?',
    userId: 'employee_123',
    sessionId: 'session_abc'
  });
  
  console.log('Response:', response.data.response);
  console.log('Intent:', response.data.intent);
  console.log('Confidence:', response.data.confidence);
} catch (error) {
  console.error('Error:', error.message);
}

// Get employee info
try {
  const employee = await client.employees.get('employee_123');
  console.log('Employee:', employee.data.name);
  console.log('Department:', employee.data.department);
} catch (error) {
  console.error('Error:', error.message);
}
```

### cURL Examples

#### Send Chat Message
```bash
curl -X POST "https://your-domain.com/api/v1/chat/message/" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Berapa sisa cuti saya?",
    "user_id": "employee_123",
    "session_id": "session_abc123"
  }'
```

#### Get Employee Info
```bash
curl -X GET "https://your-domain.com/api/v1/employees/employee_123/" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

#### Get Analytics
```bash
curl -X GET "https://your-domain.com/api/v1/analytics/chat/?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Webhook Integration

#### Setup Webhook
```python
# Configure webhook endpoint
client.webhooks.create({
    'url': 'https://your-app.com/webhooks/hrbot/',
    'events': ['message.received', 'intent.detected'],
    'secret': 'your-webhook-secret'
})
```

#### Handle Webhook
```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhooks/hrbot/', methods=['POST'])
def handle_webhook():
    # Verify signature
    signature = request.headers.get('X-HRBot-Signature')
    payload = request.get_data()
    
    expected_signature = hmac.new(
        b'your-webhook-secret',
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, f'sha256={expected_signature}'):
        return 'Invalid signature', 401
    
    # Process webhook data
    data = request.get_json()
    event_type = data.get('event')
    
    if event_type == 'message.received':
        # Handle new message
        message = data.get('data')
        print(f"New message: {message['text']}")
    
    return 'OK', 200
```

---

**API Reference Version**: 1.0  
**Last Updated**: Januari 2025  
**Support**: api-support@your-domain.com