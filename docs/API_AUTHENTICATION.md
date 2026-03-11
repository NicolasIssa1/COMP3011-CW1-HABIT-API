# API Authentication Guide

## Overview

The Habit & Productivity Analytics API uses **API Key authentication** via the `X-API-Key` header. All requests (except `/health` and `/`) must include a valid API key.

## Authentication Methods

### Using cURL

```bash
curl -H "X-API-Key: test-api-key-12345" https://api.example.com/habits
```

### Using Python (requests)

```python
import requests

headers = {"X-API-Key": "test-api-key-12345"}
response = requests.get("https://api.example.com/habits", headers=headers)
```

### Using JavaScript (fetch)

```javascript
const apiKey = "test-api-key-12345";

fetch("https://api.example.com/habits", {
    headers: {
        "X-API-Key": apiKey,
        "Content-Type": "application/json"
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

## API Keys

### Development

| Key | Usage | Expiry |
|-----|-------|--------|
| `test-api-key-12345` | Testing, local development | Never |

### Production

API keys for production are provided separately. Set the `API_KEY` environment variable:

```bash
export API_KEY="your-production-key"
```

## Error Responses

### Missing API Key (401 Unauthorized)

```http
GET /habits
```

**Response:**
```json
{
  "detail": "Missing API key. Include X-API-Key header."
}
```

### Invalid API Key (403 Forbidden)

```http
GET /habits
X-API-Key: wrong-key
```

**Response:**
```json
{
  "detail": "Invalid API key."
}
```

## Public Endpoints

The following endpoints do **not** require authentication:

- `GET /` — API info
- `GET /health` — Health check

All other endpoints require the `X-API-Key` header.

## Configuration

Set your API key via environment variable:

```bash
# .env
API_KEY=your-secret-key-here
```

If not provided, defaults to `test-api-key-12345` (development only).

## Security Notes

- ⚠️ **Never commit API keys** to version control
- ⚠️ **Use HTTPS in production** to prevent key interception
- ⚠️ **Rotate keys regularly** if compromised
- ⚠️ **Keep keys secret** — treat them like passwords
