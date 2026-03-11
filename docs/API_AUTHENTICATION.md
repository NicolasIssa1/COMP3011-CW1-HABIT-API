# API Authentication Guide

## Overview

The Habit & Productivity Analytics API uses **API Key authentication** via the `X-API-Key` header. All requests to `/api/...` endpoints require a valid API key.

**Three ways to access the API:**
1. **Web Dashboard** (`/ui/`) — Frontend app; sends X-API-Key header automatically
2. **Swagger Docs** (`/docs`) — Interactive testing; shows where to put the header
3. **Raw API** (`/api/habits`, etc.) — Programmatic access; you add the header

**All three use the exact same authentication.**

## What Requires Authentication?

**Protected endpoints** (require `X-API-Key` header):
- `POST /api/habits` — create
- `GET /api/habits` — list  
- `GET /api/habits/{id}` — read
- `PATCH /api/habits/{id}` — update
- `DELETE /api/habits/{id}` — delete
- `POST /api/habits/{id}/logs` — log completion
- `GET /api/habits/{id}/logs` — list logs
- `DELETE /api/habits/{id}/logs/{id}` — delete log
- `GET /api/habits/{id}/streak` — get streak stats
- `GET /api/analytics/weekly-summary` — get weekly analytics

**Public endpoints** (no authentication required):
- `GET /` — API info
- `GET /health` — Health check

## Using In Different Contexts

### 1. Web Dashboard (`/ui/`)

```
You fill form → Click button → App automatically adds X-API-Key header → Request sent
```

- No manual header setup needed
- API key input field at top of page (default: `test-api-key-12345`)
- Key is read from input on every request

**Example:** Create a habit via dashboard → Behind scenes: `POST /api/habits with X-API-Key: test-api-key-12345`

### 2. Swagger Docs (`/docs`)

```
Open /docs → Find endpoint → Click "Try it out" → Fill parameters → Execute
```

- Swagger automatically handles the X-API-Key header
- You don't type the header manually
- Just supply the request body
- See live responses

**Example:** Test via /docs → Click `GET /api/habits` → Execute → See results

### 3. Adding the Header Manually (Programmatic)

For command line, scripts, or custom applications, you must add the `X-API-Key` header yourself.

#### Using cURL

```bash
curl -H "X-API-Key: test-api-key-12345" http://localhost:8000/api/habits
```

#### Using Python (requests)

```python
import requests

headers = {"X-API-Key": "test-api-key-12345"}
response = requests.get("http://localhost:8000/api/habits", headers=headers)
print(response.json())
```

#### Using JavaScript (fetch)

```javascript
const apiKey = "test-api-key-12345";

fetch("http://localhost:8000/api/habits", {
    method: "GET",
    headers: {
        "X-API-Key": apiKey,
        "Content-Type": "application/json"
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));
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

When you try to access a protected endpoint without the `X-API-Key` header:

```bash
curl http://localhost:8000/api/habits
```

**Response:**
```json
{
  "detail": "Missing API key. Include X-API-Key header."
}
```

**Fix:** Add the header: `curl -H "X-API-Key: test-api-key-12345" http://localhost:8000/api/habits`

### Invalid API Key (403 Forbidden)

When you provide an incorrect API key:

```bash
curl -H "X-API-Key: wrong-key" http://localhost:8000/api/habits
```

**Response:**
```json
{
  "detail": "Invalid API key."
}
```

**Fix:** Check the API key matches the server configuration. Default for development is `test-api-key-12345`.

## Summary: When To Use Which Interface

| Interface | Use Case | Auth Required |
|-----------|----------|---------------|
| `/ui/` | User-friendly dashboard for habit tracking | Yes, via input field |
| `/docs` | Interactive documentation and endpoint testing | Yes, but Swagger handles it |
| Raw `/api/` | Programmatic access from scripts/apps | Yes, you add header |
| `/health` | Health checks | No |

## Configuration

Set your API key via environment variable when running locally:

```bash
# Default for development
API_KEY=test-api-key-12345

# Or set in .env
DATABASE_URL=sqlite:///./dev.db
API_KEY=test-api-key-12345
ENVIRONMENT=development
```

Then run:
```bash
python -m uvicorn app.main:app --reload
```

**Default key:** `test-api-key-12345` (development only)  
**Production:** Set `API_KEY` environment variable to a secure value

## Security Notes

- ⚠️ **Never commit API keys** to version control
- ⚠️ **Use HTTPS in production** to prevent key interception
- ⚠️ **Rotate keys regularly** if compromised
- ⚠️ **Keep keys secret** — treat them like passwords
