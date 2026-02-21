---
name: publora-linkedin
description: >
  Post or schedule content to LinkedIn using the Publora API. Use this skill
  when the user wants to publish, schedule, or draft a LinkedIn post via Publora.
---

# Publora — LinkedIn

Post and schedule LinkedIn content via the Publora API.

> **Prerequisite:** Install the `publora` core skill for auth setup and getting platform IDs.

## Get Your LinkedIn Platform ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries with "linkedin" in the id, e.g. "linkedin-ABC123"
```

## Post to LinkedIn Immediately

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Excited to share our latest update! 🚀\n\nWe just launched...',
    platforms: ['linkedin-ABC123']
  })
});
```

## Schedule a LinkedIn Post

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Monday thought: consistency beats perfection every time. 💡',
    platforms: ['linkedin-ABC123'],
    scheduledTime: '2026-03-16T09:00:00.000Z'
  })
});
// Response: { postGroupId: "pg_abc123", scheduledTime: "..." }
```

## LinkedIn + Image

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Our team at the conference! Great connections made today.',
    'platforms': ['linkedin-ABC123'],
    'scheduledTime': '2026-03-16T09:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'team-photo.jpg', 'contentType': 'image/jpeg',
    'type': 'image', 'postGroupId': post['postGroupId']
}).json()

# Step 3: Upload to S3
with open('team-photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Tips for LinkedIn

- **Best times:** Tuesday–Thursday, 8–10 AM or 12 PM in your audience's timezone
- **Optimal length:** 1,300–2,000 characters for thought leadership posts
- **Line breaks matter:** LinkedIn shows ~3 lines before "see more" — hook early
- **Markdown:** LinkedIn doesn't render markdown; avoid `**bold**` syntax in content
- **Hashtags:** 3–5 relevant hashtags at the end perform best
