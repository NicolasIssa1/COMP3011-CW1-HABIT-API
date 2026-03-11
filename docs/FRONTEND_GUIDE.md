# Front-End Guide

## Overview

The Habit Dashboard is a minimal, responsive single-page application (SPA) built with vanilla HTML, CSS, and JavaScript. It provides a user-friendly interface to interact with the Habit & Productivity Analytics API.

**Important:** The dashboard (`/ui/`) is a **frontend consumer** of the same backend API that powers the Swagger docs (`/docs`). Everything it does goes through the `/api/...` routes.

## Quick Architecture

```
You (User)
  ↓
/ui/ Dashboard (HTML/CSS/JavaScript)
  ↓
/api/habits, /api/analytics/... (Backend routes)
  ↓
Database
```

When you **Create a Habit** in the dashboard:
```
1. You fill the form (name, description, frequency)
2. Click "Create Habit"
3. Dashboard sends: POST /api/habits (with X-API-Key header)
4. Backend creates habit and returns it
5. Dashboard shows it in list
```

**Same flow for all operations** (list, delete, mark done, view stats).

## Accessing the Dashboard

Once the API is running, access the dashboard at:

```
http://localhost:8000/ui/
```

Or on Render:

```
https://comp3011-cw1-habit-api.onrender.com/ui/
```

**Authentication:** Default API key `test-api-key-12345` is pre-filled. You can change it at the top of the page if needed.

**Related Resources:**
- **Test endpoints directly:** http://localhost:8000/docs (Swagger UI)
- **Call API from code:** Use `/api/habits`, `/api/analytics/...` with `X-API-Key` header

## Features

### 1. API Key Configuration

**Section:** Top of page  
**Purpose:** Set your API key for authentication

- Default key for development: `test-api-key-12345`
- Change the key before request if needed
- Key is stored in browser memory (cleared on page refresh)

![API Key Input](./screenshots/api-key.png)

### 2. Create Habit

**Section:** Left panel  
**Purpose:** Add a new habit to track

**Fields:**
- **Habit Name** (required): Name of the habit (e.g., "Morning Exercise")
- **Description** (optional): Details (e.g., "30 minutes of cardio")
- **Frequency** (required): daily, weekly, or monthly

**Example:**
```
Name: Drink Water
Description: 8 glasses per day
Frequency: Daily
```

### 3. Habits List

**Section:** Main panel  
**Purpose:** View and manage all habits

**Actions per habit:**
- **✓ Mark Done Today** — Log today's completion
- **📊 Stats** — View streak and analytics
- **🗑️ Delete** — Remove the habit

**Search:** Filter habits by name or description in real-time

### 4. Analytics

**Section:** Right panel  
**Purpose:** View performance metrics for a specific habit

**Metrics:**
- **Current Streak:** Days in a row of completion
- **Longest Streak:** Best streak ever
- **Total Completions:** All-time completion count

**Selection:** Choose a habit from the dropdown to view stats

## What Happens When You...

### Create a habit

1. Fill the form with name, description, and frequency
2. Click "Create Habit"
3. Habit appears in the list
4. Form clears for next entry

### Mark a habit as done today

1. Find the habit in the list
2. Click "✓ Mark Done Today"
3. If already logged today: "Already logged for today!" message
4. If successful: "Habit marked as done! 🎉" message

### View stats

1. Click "📊 Stats" on a habit, OR
2. Select from "Analytics" dropdown in the right panel
3. Current and longest streak appear below

### Delete a habit

1. Click "🗑️ Delete" on the habit
2. Confirm the deletion
3. Habit is removed from list and database

## Error Messages

| Message | Meaning | Action |
|---------|---------|--------|
| "Missing API key" | No X-API-Key header | Ensure API key is set |
| "Invalid API key" | Wrong key provided | Check key matches server config |
| "Habit marked as done! 🎉" | Success | Normal operation |
| "Already logged for today!" | Duplicate log | Can only log once per day |
| "Failed to create habit: ..." | Creation error | Check input and try again |

## Technical Details

### Architecture

The dashboard communicates with the backend via REST API calls:

```
Dashboard (app.js)
├─ API_BASE = "/api"
│
├─ GET /api/habits
├─ POST /api/habits (create)
├─ DELETE /api/habits/{id} (delete)
├─ POST /api/habits/{id}/logs (mark done)
├─ GET /api/habits/{id}/streak (get stats)
├─ GET /api/analytics/weekly-summary
│
└─ All endpoints include X-API-Key header
    └─ headers: { X-API-Key: <value from input> }
```

**Same Endpoints Tested In:**
- **`/docs`** (Swagger UI) — Try manually
- **`/ui/`** (Dashboard) — Try via buttons
- **Raw API** — Call from code

### How Data Flows

```
User Input (form submit, button click)
    ↓
Event Handler in app.js
    ↓
Validate & prepare data
    ↓
Call apiRequest(method, endpoint, body)
    ↓
Fetch API (with X-API-Key header)
    ↓
Backend processes at /api/...
    ↓
Return JSON response
    ↓
Display result or error message
```

## Technical Details: API Key Handling

**Read from:** Input field at top of page (default: `test-api-key-12345`)  
**Included in:** Every request in `X-API-Key` header  
**Expires:** Never (for development)  
**Production:** Use environment variable instead  

All API calls use this header:
```javascript
headers: {
    "X-API-Key": getApiKey(),
    "Content-Type": "application/json"
}
```

## Responsive Design

The dashboard is optimized for:

- **Desktop:** Large grid layout (2 columns)
- **Tablet:** Responsive grid (1-2 columns)
- **Mobile:** Full-width single column

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Requires ES6 support

## Troubleshooting

### "Missing API key" errors

**Problem:** Requests fail with 401  
**Solution:** Enter API key in the input field at the top

### "Invalid API key" errors

**Problem:** Requests fail with 403  
**Solution:** Check API key matches the server config

### No habits appear

**Problem:** Empty list / "No habits yet" message  
**Solution:** Create a habit using the form to get started

### Analytics not loading

**Problem:** "Failed to load analytics" message  
**Solution:** Select a habit from the dropdown

### Slow performance

**Problem:** Dashboard feels sluggish  
**Solution:** Check network tab for slow API responses

## Browser Developer Tools

Open `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac):

- **Console:** See debug messages and errors
- **Network:** Monitor API requests
- **Application:** Check stored data

Example console output:

```javascript
// Check API key
console.log(getApiKey());

// Test API call
apiRequest("GET", "/habits").then(data => console.log(data));
```

## Future Enhancements

Potential features (not in current version):

- [ ] Recurring habits with rest days
- [ ] Habit reminders/notifications
- [ ] Data export (CSV, PDF)
- [ ] Dark mode
- [ ] User accounts / multi-user
- [ ] Mobile app

---

**Version:** 1.0  
**Last Updated:** March 11, 2026
