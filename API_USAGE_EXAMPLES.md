# API Usage Examples for Multi-Language Posts

## Base URL
```
http://localhost:8000/api/posts/
```

## Language Parameter
All endpoints support the `lang` query parameter:
- `lang=uz` - Uzbek (default)
- `lang=ru` - Russian
- `lang=en` - English

## Endpoints

### 1. Get All Posts
```http
GET /api/posts/?lang=ru
```

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/posts/?page=2&lang=ru",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Заголовок новости",  // In Russian
      "slug": "novost-1",
      "category": {
        "id": 1,
        "name": "News",
        "type": "news"
      },
      "short_description": "Краткое описание",
      "image": "http://localhost:8000/media/post_images/image.jpg",
      "video_url": null,
      "video_file": "http://localhost:8000/media/post_videos/video.mp4",
      "type_tag": "Technology",
      "published_at": "2026-01-18T10:00:00Z",
      "created_at": "2026-01-18T09:00:00Z",
      "views_count": 150
    }
  ]
}
```

### 2. Get Single Post
```http
GET /api/posts/{slug}/?lang=en
```

**Response:**
```json
{
  "id": 1,
  "title": "News Title",  // In English
  "slug": "yangilik-1",
  "category": {...},
  "short_description": "Brief description",
  "content": "Full article content in English...",
  "image": "http://localhost:8000/media/post_images/image.jpg",
  "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "video_file": null,
  "type_tag": "Technology",
  "status": "published",
  "published_at": "2026-01-18T10:00:00Z",
  "created_at": "2026-01-18T09:00:00Z",
  "updated_at": "2026-01-18T09:30:00Z",
  "views_count": 151
}
```

### 3. Get Latest News
```http
GET /api/posts/latest-news/?lang=uz
```

Returns 15 most recent news posts in Uzbek.

### 4. Get News (Paginated)
```http
GET /api/posts/news/?lang=ru&page=1&page_size=12
```

Returns paginated news posts in Russian.

### 5. Get Announcements
```http
GET /api/posts/announcements/?lang=en
```

### 6. Get Latest Announcements
```http
GET /api/posts/latest-announcements/?lang=uz
```

Returns 4 most recent announcements.

### 7. Get Media/Videos
```http
GET /api/posts/media/?lang=ru
```

### 8. Get Latest Videos
```http
GET /api/posts/latest-videos/?lang=en
```

Returns 4 most recent video posts.

### 9. Get Reports
```http
GET /api/posts/reports/?lang=uz
```

### 10. Search Posts
```http
GET /api/posts/search/?q=technology&lang=en
```

**Note:** Search works across ALL language fields, regardless of the `lang` parameter.

## React Integration Examples

### Using Fetch API

```javascript
// Get posts in user's selected language
const fetchPosts = async (language = 'uz') => {
  const response = await fetch(`/api/posts/?lang=${language}`);
  const data = await response.json();
  return data;
};

// Get single post
const fetchPost = async (slug, language = 'uz') => {
  const response = await fetch(`/api/posts/${slug}/?lang=${language}`);
  const data = await response.json();
  return data;
};

// Search posts
const searchPosts = async (query, language = 'uz') => {
  const response = await fetch(
    `/api/posts/search/?q=${encodeURIComponent(query)}&lang=${language}`
  );
  const data = await response.json();
  return data;
};
```

### Using Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Get posts with language
export const getPosts = (language = 'uz', page = 1) => {
  return api.get('/posts/', {
    params: { lang: language, page }
  });
};

// Get latest news
export const getLatestNews = (language = 'uz') => {
  return api.get('/posts/latest-news/', {
    params: { lang: language }
  });
};

// Search
export const searchPosts = (query, language = 'uz') => {
  return api.get('/posts/search/', {
    params: { q: query, lang: language }
  });
};
```

### React Component Example

```jsx
import React, { useState, useEffect } from 'react';

const NewsList = () => {
  const [posts, setPosts] = useState([]);
  const [language, setLanguage] = useState('uz');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:8000/api/posts/latest-news/?lang=${language}`
        );
        const data = await response.json();
        setPosts(data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [language]);

  return (
    <div>
      {/* Language selector */}
      <select 
        value={language} 
        onChange={(e) => setLanguage(e.target.value)}
      >
        <option value="uz">O'zbek</option>
        <option value="ru">Русский</option>
        <option value="en">English</option>
      </select>

      {/* Posts list */}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div>
          {posts.map(post => (
            <article key={post.id}>
              <h2>{post.title}</h2>
              {post.image && (
                <img src={post.image} alt={post.title} />
              )}
              <p>{post.short_description}</p>
              
              {/* Video handling */}
              {post.video_url && (
                <iframe src={post.video_url} />
              )}
              {post.video_file && (
                <video src={post.video_file} controls />
              )}
              
              <time>{new Date(post.published_at).toLocaleDateString()}</time>
              <span>👁️ {post.views_count} views</span>
            </article>
          ))}
        </div>
      )}
    </div>
  );
};

export default NewsList;
```

### Context API for Language Management

```jsx
// LanguageContext.js
import React, { createContext, useState, useContext } from 'react';

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(
    localStorage.getItem('language') || 'uz'
  );

  const changeLanguage = (lang) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
  };

  return (
    <LanguageContext.Provider value={{ language, changeLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
```

```jsx
// Using the context
import { useLanguage } from './LanguageContext';

const PostDetail = ({ slug }) => {
  const { language } = useLanguage();
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch(`/api/posts/${slug}/?lang=${language}`)
      .then(res => res.json())
      .then(data => setPost(data));
  }, [slug, language]);

  // Render post...
};
```

## Important Notes

### Video Display Logic
```javascript
// Always check both video_url and video_file
const VideoPlayer = ({ post }) => {
  if (post.video_url) {
    // External video (YouTube, etc.)
    return <iframe src={post.video_url} />;
  } else if (post.video_file) {
    // Uploaded video file
    return <video src={post.video_file} controls />;
  }
  return null;
};
```

### Language Fallback
The API automatically handles fallback:
- If content not available in requested language, returns Uzbek
- If Uzbek not available, tries Russian
- If Russian not available, tries English
- Frontend always receives valid content

### Search Behavior
Search works across ALL languages:
```javascript
// Search for "технология" will find posts with this word
// in ANY language field (title_ru, content_ru, etc.)
const results = await searchPosts('технология', 'ru');
// Will return posts in Russian, but found across all languages
```

## Performance Tips

1. **Use pagination** for large lists
2. **Cache language preference** in localStorage
3. **Lazy load images and videos**
4. **Use React Query or SWR** for better data fetching
5. **Implement infinite scroll** for better UX

## Error Handling

```javascript
const fetchPostsWithErrorHandling = async (language = 'uz') => {
  try {
    const response = await fetch(`/api/posts/?lang=${language}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    console.error('Error fetching posts:', error);
    return { data: null, error: error.message };
  }
};
```
