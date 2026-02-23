---
name: publora-threads
description: >
  Post or schedule content to Threads using the Publora API. Use this skill
  when the user wants to publish or schedule a Threads post via Publora.
---

# Publora — Threads

Post and schedule Threads content via the Publora API.

> **Prerequisite:** Install the `publora` core skill for auth setup and getting platform IDs.

## Get Your Threads Platform ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "threads-789"
```

## Post to Threads Immediately

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Good morning Threads 👋 What are you building today?',
    platforms: ['threads-789']
  })
});
```

## Schedule a Threads Post

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Reminder: ship it, then make it perfect. Done beats perfect.',
    platforms: ['threads-789'],
    scheduledTime: '2026-03-16T11:00:00.000Z'
  })
});
```

## Threads + Image

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Behind the scenes 👇',
    'platforms': ['threads-789'],
    'scheduledTime': '2026-03-16T11:00:00.000Z'
}).json()

upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'behind-scenes.jpg', 'contentType': 'image/jpeg',
    'type': 'image', 'postGroupId': post['postGroupId']
}).json()

with open('behind-scenes.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Tips for Threads

- **Conversational tone** works best — Threads rewards authenticity over polish
- **500 character limit** per post
- **Best times:** Morning (7–9 AM) and evening (7–9 PM)
- **No hashtags** — Threads doesn't surface content via hashtags the same way
- **Cross-post with Instagram** for wider reach on Meta platforms
