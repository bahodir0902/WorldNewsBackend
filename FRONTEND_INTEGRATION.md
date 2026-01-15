# Frontend Integration Examples

This file shows exactly how to update your React frontend components to use the backend API.

## 1. Create API Service

Create a new file: `frontend/src/services/api.ts`

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface Post {
  id: number;
  title: string;
  slug: string;
  category: {
    id: number;
    name: string;
    type: string;
    description: string;
  } | null;
  short_description: string;
  content?: string;
  image: string | null;
  video_url: string | null;
  type_tag: string;
  published_at: string;
  created_at: string;
  views_count: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Homepage APIs
export const fetchLatestNews = async (): Promise<Post[]> => {
  const response = await fetch(`${API_BASE_URL}/posts/latest-news/`);
  if (!response.ok) throw new Error('Failed to fetch latest news');
  return response.json();
};

export const fetchLatestAnnouncements = async (): Promise<Post[]> => {
  const response = await fetch(`${API_BASE_URL}/posts/latest-announcements/`);
  if (!response.ok) throw new Error('Failed to fetch announcements');
  return response.json();
};

export const fetchLatestVideos = async (): Promise<Post[]> => {
  const response = await fetch(`${API_BASE_URL}/posts/latest-videos/`);
  if (!response.ok) throw new Error('Failed to fetch videos');
  return response.json();
};

// Page APIs
export const fetchNews = async (page: number = 1): Promise<PaginatedResponse<Post>> => {
  const response = await fetch(`${API_BASE_URL}/posts/news/?page=${page}`);
  if (!response.ok) throw new Error('Failed to fetch news');
  return response.json();
};

export const fetchAnnouncements = async (page: number = 1): Promise<PaginatedResponse<Post>> => {
  const response = await fetch(`${API_BASE_URL}/posts/announcements/?page=${page}`);
  if (!response.ok) throw new Error('Failed to fetch announcements');
  return response.json();
};

export const fetchMedia = async (page: number = 1): Promise<PaginatedResponse<Post>> => {
  const response = await fetch(`${API_BASE_URL}/posts/media/?page=${page}`);
  if (!response.ok) throw new Error('Failed to fetch media');
  return response.json();
};

export const fetchReports = async (page: number = 1): Promise<PaginatedResponse<Post>> => {
  const response = await fetch(`${API_BASE_URL}/posts/reports/?page=${page}`);
  if (!response.ok) throw new Error('Failed to fetch reports');
  return response.json();
};

// Post detail
export const fetchPostDetail = async (slug: string): Promise<Post> => {
  const response = await fetch(`${API_BASE_URL}/posts/${slug}/`);
  if (!response.ok) throw new Error('Failed to fetch post detail');
  return response.json();
};

// Search
export const searchPosts = async (query: string, page: number = 1): Promise<PaginatedResponse<Post>> => {
  const response = await fetch(`${API_BASE_URL}/posts/search/?q=${encodeURIComponent(query)}&page=${page}`);
  if (!response.ok) throw new Error('Failed to search posts');
  return response.json();
};
```

## 2. Update Environment Variables

Create/update `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

## 3. Update OfficialAnnouncements.tsx

```typescript
import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { fetchLatestAnnouncements, Post } from "../../services/api"

export const OfficialAnnouncements = () => {
  const {t} = useTranslation()
  const [data, setData] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchLatestAnnouncements()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  const title = {
    value : t("home.paragraph.official")
  }
  
  return (
    <div className="flex flex-col gap-y-5">
      <div className="py-3 border-b-4  border-[#1E6FDA]">
        <p className="font-bold text-black text-3xl font-serif tracking-wide">{title.value}</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4  gap-y-3   gap-x-3 ">
        {data.map((res) => (
          <div key={res.id} className="flex flex-col bg-white justify-between shadow-md shadow-zinc-400">
            <div>
              <div className="overflow-hidden">
                <img
                  src={res.image || "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80"}
                  className="w-full cursor-pointer object-cover h-40 transition-transform duration-500 hover:scale-110"
                  alt={res.title}
                />
              </div>
            </div>
            <div className="p-3 flex pb-5 flex-col gap-y-5 h-full justify-between ">
              <p className="text-black text-2xl font-bold line-clamp-3">
                {res.title}
              </p>
              <p className="text-sm text-zinc-500">
                {new Date(res.published_at).toLocaleDateString('en-US', { 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 4. Update NewsH.tsx

```typescript
import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { fetchLatestNews, Post } from "../../services/api"

export const NewsH = () => {
  const {t} = useTranslation()
  const [data, setData] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLatestNews()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  const title = {
    value : t("home.paragraph.news")
  }

  if (loading) return <div>Loading news...</div>

  return (
    <div className="flex flex-col gap-y-5">
      <div className="py-3 border-b-4  border-[#1E6FDA]">
        <p className="font-bold text-black text-3xl font-serif tracking-wide">{title.value}</p>
      </div>
      <div className="flex flex-col rounded-md border border-zinc-200 bg-white">
        {data.map((res) => (
          <div key={res.id} className="p-5 flex flex-col gap-y-5 hover:bg-blue-50 cursor-pointer bg-transparent border-b border-zinc-200 ">
            <div className="flex items-start gap-x-3  ">
              {res.image && (
                <div>
                  <img
                    src={res.image}
                    className="w-150 md:w-30 h-20 md:h-20 object-cover rounded-md"
                    alt={res.title}
                  />
                </div>
              )}
              <div className="flex flex-col gap-y-5">
                <p className="text-[#142543] text-2xl line-clamp-2 font-bold font-serif ">{res.title}</p>
                <div className="hidden md:flex  gap-x-3 items-center ">
                  <p className="bg-blue-100 text-[#1E6FDA] px-2 py-1 rounded-md text-xs flex justify-center items-center font-semibold">
                    {res.type_tag || res.category?.name || 'News'}
                  </p>
                  <p className="text-xs text-zinc-500">
                    {new Date(res.published_at).toLocaleDateString('en-US', { 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </p>
                </div>
              </div>
            </div>
            <div className="flex md:hidden  gap-x-3 items-center ">
              <p className="bg-blue-100 text-[#1E6FDA] px-2 py-1 rounded-md text-xs flex justify-center items-center font-semibold">
                {res.type_tag || res.category?.name || 'News'}
              </p>
              <p className="text-xs text-zinc-500">
                {new Date(res.published_at).toLocaleDateString('en-US', { 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 5. Update Video.tsx

```typescript
import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { fetchLatestVideos, Post } from "../../services/api"

export const Video = () => {
  const {t} = useTranslation()
  const [data, setData] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLatestVideos()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  const title = {
    value : t("home.paragraph.video")
  }

  if (loading) return <div>Loading videos...</div>

  return (
    <div className="flex flex-col gap-y-5">
      <div className="py-3 border-b-4  border-[#1E6FDA]">
        <p className="font-bold text-black text-3xl font-serif tracking-wide">{title.value}</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {data.map((item) => (
          <div
            key={item.id}
            className="bg-white  shadow-md shadow-zinc-300 hover:shadow-md transition cursor-pointer"
          >
            <div className="relative overflow-hidden">
              <img
                src={item.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80"}
                className="w-full h-35  object-cover transition-transform duration-300 hover:scale-110"
                alt={item.title}
              />

              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-14 h-14 bg-white/90 group hover:bg-amber-500 duration-300  rounded-full flex items-center justify-center">
                  <div className="w-0 h-0 border-l-12 group-hover:text-white  border-y-8 border-y-transparent ml-1"></div>
                </div>
              </div>
            </div>

            <div className="p-4">
              <p className="font-semibold text-sm text-[#142543]  line-clamp-2">
                {item.title}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 6. Update News.tsx (Full Page)

```typescript
import { useEffect, useState } from "react"
import { fetchNews, Post, PaginatedResponse } from "../services/api"

export const News = () => {
  const [data, setData] = useState<PaginatedResponse<Post> | null>(null)
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)

  useEffect(() => {
    setLoading(true)
    fetchNews(page)
      .then(setData)
      .finally(() => setLoading(false))
  }, [page])

  if (loading) return <div className="p-10 text-center">Loading news...</div>

  return (
    <div className="p-5">
      <h1 className="text-4xl font-bold mb-5">News</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {data?.results.map((post) => (
          <div key={post.id} className="bg-white shadow-md rounded-md overflow-hidden">
            {post.image && (
              <img 
                src={post.image} 
                alt={post.title}
                className="w-full h-48 object-cover"
              />
            )}
            <div className="p-4">
              <h2 className="text-xl font-bold mb-2">{post.title}</h2>
              <p className="text-gray-600 mb-3">{post.short_description}</p>
              <div className="flex justify-between items-center">
                <span className="bg-blue-100 text-blue-600 px-2 py-1 rounded text-sm">
                  {post.type_tag || post.category?.name}
                </span>
                <span className="text-sm text-gray-500">
                  {new Date(post.published_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {data && (
        <div className="flex justify-center gap-3 mt-10">
          <button 
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={!data.previous}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
          >
            Previous
          </button>
          <span className="px-4 py-2">Page {page}</span>
          <button 
            onClick={() => setPage(p => p + 1)}
            disabled={!data.next}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}
```

## 7. Similar Updates for Other Pages

### Announcements.tsx
```typescript
// Same structure as News.tsx but use fetchAnnouncements instead of fetchNews
```

### Media.tsx
```typescript
// Same structure as News.tsx but use fetchMedia instead of fetchNews
```

### Reports.tsx
```typescript
// Same structure as News.tsx but use fetchReports instead of fetchNews
```

## 8. Add Post Detail Page (Optional)

Create `frontend/src/pages/PostDetail.tsx`:

```typescript
import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { fetchPostDetail, Post } from "../services/api"

export const PostDetail = () => {
  const { slug } = useParams<{ slug: string }>()
  const [post, setPost] = useState<Post | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (slug) {
      fetchPostDetail(slug)
        .then(setPost)
        .finally(() => setLoading(false))
    }
  }, [slug])

  if (loading) return <div className="p-10 text-center">Loading...</div>
  if (!post) return <div className="p-10 text-center">Post not found</div>

  return (
    <div className="max-w-4xl mx-auto p-5">
      {post.image && (
        <img 
          src={post.image} 
          alt={post.title}
          className="w-full h-96 object-cover rounded-lg mb-5"
        />
      )}
      
      <h1 className="text-4xl font-bold mb-3">{post.title}</h1>
      
      <div className="flex gap-3 mb-5">
        <span className="bg-blue-100 text-blue-600 px-3 py-1 rounded">
          {post.type_tag || post.category?.name}
        </span>
        <span className="text-gray-500">
          {new Date(post.published_at).toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </span>
        <span className="text-gray-500">{post.views_count} views</span>
      </div>

      <div className="prose max-w-none">
        <p className="text-lg text-gray-700 mb-4">{post.short_description}</p>
        <div className="whitespace-pre-wrap">{post.content}</div>
      </div>

      {post.video_url && (
        <div className="mt-5">
          <iframe
            width="100%"
            height="500"
            src={post.video_url}
            title={post.title}
            allowFullScreen
            className="rounded-lg"
          />
        </div>
      )}
    </div>
  )
}
```

Then update `App.tsx`:

```typescript
import { PostDetail } from "./pages/PostDetail"

// Add route
<Route path="/posts/:slug" element={<PostDetail />} />
```

## 9. Error Handling Hook (Optional)

Create `frontend/src/hooks/useApi.ts`:

```typescript
import { useState, useEffect } from 'react'

export function useApi<T>(apiFunc: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    
    apiFunc()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { data, loading, error }
}

// Usage:
// const { data, loading, error } = useApi(fetchLatestNews)
```

## 10. CORS Configuration

Make sure your backend `.env` has:

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

And restart the backend after changing this.

---

## Testing

1. Start backend: `docker-compose up` or `python manage.py runserver`
2. Start frontend: `npm run dev`
3. Open http://localhost:5173
4. Check browser console for any errors
5. Verify data loads on homepage
6. Test navigation to each page
7. Verify images display correctly

---

## Common Issues

### CORS Errors
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in backend `.env`
- Restart backend

### Images Not Loading
- Check image URLs in network tab
- Verify backend is serving media files correctly
- Check `USE_S3_STORAGE` setting

### TypeScript Errors
- Make sure types match the API response
- Check the Post interface definition

---

That's it! Your frontend should now be fully integrated with the backend.

