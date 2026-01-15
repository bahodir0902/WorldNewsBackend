# API Endpoints Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
Currently, all endpoints are publicly accessible (no authentication required for reading).

---

## Posts Endpoints

### 1. List All Posts (Paginated)
**Endpoint:** `GET /api/posts/`

**Description:** Get paginated list of all published posts

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 12, max: 100)

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Sample News Title",
      "slug": "sample-news-title",
      "category": {
        "id": 1,
        "name": "News",
        "type": "news",
        "description": "General news articles"
      },
      "short_description": "Brief description...",
      "image": "http://localhost:8000/media/post/image.jpg",
      "video_url": null,
      "type_tag": "Education",
      "published_at": "2026-01-15T10:30:00Z",
      "created_at": "2026-01-15T10:00:00Z",
      "views_count": 150
    }
  ]
}
```

---

### 2. Get Post Detail
**Endpoint:** `GET /api/posts/{slug}/`

**Description:** Get detailed information about a specific post

**Response:**
```json
{
  "id": 1,
  "title": "Sample News Title",
  "slug": "sample-news-title",
  "category": {
    "id": 1,
    "name": "News",
    "type": "news",
    "description": "General news articles"
  },
  "short_description": "Brief description...",
  "content": "Full content of the post...",
  "image": "http://localhost:8000/media/post/image.jpg",
  "video_url": null,
  "type_tag": "Education",
  "status": "published",
  "published_at": "2026-01-15T10:30:00Z",
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-01-15T10:30:00Z",
  "views_count": 151
}
```

---

### 3. List News Posts
**Endpoint:** `GET /api/posts/news/`

**Description:** Get all posts categorized as "News" (paginated)

**Query Parameters:** Same as List All Posts

**Response:** Same structure as List All Posts

---

### 4. Latest News (Homepage)
**Endpoint:** `GET /api/posts/latest-news/`

**Description:** Get the latest 15 news articles for homepage display

**Response:**
```json
[
  {
    "id": 1,
    "title": "Latest News Title",
    "slug": "latest-news-title",
    "category": {...},
    "short_description": "Brief description...",
    "image": "http://localhost:8000/media/post/image.jpg",
    "video_url": null,
    "type_tag": "Education",
    "published_at": "2026-01-15T10:30:00Z",
    "created_at": "2026-01-15T10:00:00Z",
    "views_count": 150
  }
  // ... up to 15 items
]
```

---

### 5. List Announcements
**Endpoint:** `GET /api/posts/announcements/`

**Description:** Get all official announcements (paginated)

**Query Parameters:** Same as List All Posts

**Response:** Same structure as List All Posts

---

### 6. Latest Announcements (Homepage)
**Endpoint:** `GET /api/posts/latest-announcements/`

**Description:** Get the latest 4 official announcements for homepage display

**Response:** Array of 4 announcement objects

---

### 7. List Media/Videos
**Endpoint:** `GET /api/posts/media/`

**Description:** Get all media and video posts (paginated)

**Query Parameters:** Same as List All Posts

**Response:** Same structure as List All Posts

---

### 8. Latest Videos (Homepage)
**Endpoint:** `GET /api/posts/latest-videos/`

**Description:** Get the latest 4 videos for homepage display

**Response:** Array of 4 video post objects

---

### 9. List Reports
**Endpoint:** `GET /api/posts/reports/`

**Description:** Get all report posts (paginated)

**Query Parameters:** Same as List All Posts

**Response:** Same structure as List All Posts

---

### 10. Search Posts
**Endpoint:** `GET /api/posts/search/?q={query}`

**Description:** Search posts by title, description, or content

**Query Parameters:**
- `q`: Search query (required)
- `page`: Page number (optional)
- `page_size`: Items per page (optional)

**Example:** `GET /api/posts/search/?q=education`

**Response:** Same structure as List All Posts

---

## Categories Endpoints

### 1. List All Categories
**Endpoint:** `GET /api/categories/`

**Description:** Get all post categories

**Response:**
```json
[
  {
    "id": 1,
    "name": "News",
    "type": "news",
    "description": "General news articles"
  },
  {
    "id": 2,
    "name": "Education",
    "type": "news",
    "description": "Educational news and updates"
  },
  {
    "id": 3,
    "name": "Official Announcements",
    "type": "announcement",
    "description": "Official announcements and updates"
  },
  {
    "id": 4,
    "name": "Videos",
    "type": "media",
    "description": "Video content"
  },
  {
    "id": 5,
    "name": "Reports",
    "type": "report",
    "description": "Annual and periodic reports"
  }
]
```

---

## Frontend Integration Guide

### Homepage Integration

For the homepage, you'll need to make the following API calls:

1. **Official Announcements Section:**
   ```javascript
   fetch('http://localhost:8000/api/posts/latest-announcements/')
   ```

2. **News Section:**
   ```javascript
   fetch('http://localhost:8000/api/posts/latest-news/')
   ```

3. **Videos Section:**
   ```javascript
   fetch('http://localhost:8000/api/posts/latest-videos/')
   ```

### News Page Integration

```javascript
// For the /news page
fetch('http://localhost:8000/api/posts/news/?page=1&page_size=12')
```

### Announcements Page Integration

```javascript
// For the /announcements page
fetch('http://localhost:8000/api/posts/announcements/?page=1&page_size=12')
```

### Media Page Integration

```javascript
// For the /media page
fetch('http://localhost:8000/api/posts/media/?page=1&page_size=12')
```

### Reports Page Integration

```javascript
// For the /reports page
fetch('http://localhost:8000/api/posts/reports/?page=1&page_size=12')
```

### Post Detail Page Integration

```javascript
// For individual post pages
fetch(`http://localhost:8000/api/posts/${slug}/`)
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "detail": "Error message describing the issue"
}
```

---

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React default)

Add more origins in `.env` file:
```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://your-domain.com
```

---

## Pagination

All list endpoints support pagination:
- Default page size: 12 items
- Maximum page size: 100 items
- Use `?page=2` for next page
- Use `?page_size=20` to change items per page

---

## Image URLs

- When `USE_S3_STORAGE=False`: Images are served from local media folder
- When `USE_S3_STORAGE=True`: Images are served from AWS S3 bucket
- All image URLs in responses are absolute URLs ready to use in `<img>` tags

---

## Health Check

**Endpoint:** `GET /api/check-health/`

**Response:** `ok` (200 status)

Use this endpoint to verify the API is running.

