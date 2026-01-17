# Multi-Language & Video Upload Implementation Guide

## Overview
This document describes the implementation of two major features:
1. **Video File Upload Support** - Upload videos directly instead of using URLs only
2. **Multi-Language Support** - Support for Uzbek (main), Russian, and English content

## Changes Made

### 1. Database Model Changes (`apps/posts/models/post.py`)

#### Multi-Language Fields
- Replaced single fields with language-specific versions:
  - `title` → `title_uz`, `title_ru`, `title_en`
  - `short_description` → `short_description_uz`, `short_description_ru`, `short_description_en`
  - `content` → `content_uz`, `content_ru`, `content_en`

#### Video Upload Support
- Added `video_file` field for direct video uploads
- Kept `video_url` field for YouTube/external video links
- **Important:** Only one can be used at a time (enforced by validation)

#### Validation
- Added `clean()` method to prevent both `video_file` and `video_url` being set
- Updated `save()` method to use `title_uz` for slug generation
- Added backward compatibility properties (`title`, `short_description`, `content`)

### 2. Admin Panel Updates (`apps/posts/admin.py`)

#### Organized Fieldsets
- **Uzbek Content (Main)** - Primary language section (expanded by default)
- **Russian Content** - Collapsible section
- **English Content** - Collapsible section
- **Media Section** - Now includes both `video_url` and `video_file`

#### Search Updates
- Search now works across all language fields

#### Auto-Slug Generation
- Slug now auto-generates from `title_uz` field

### 3. API Serializer Updates (`apps/posts/serializers/post.py`)

#### Language Parameter Support
- API accepts `?lang=uz`, `?lang=ru`, or `?lang=en` query parameter
- Default language: Uzbek (`uz`)

#### Fallback Logic
If requested language content is empty, fallback chain:
1. Requested language
2. Uzbek (uz)
3. Russian (ru)
4. English (en)
5. Empty string or "Untitled"

**Example:**
```
GET /api/posts/latest-news/?lang=en
```
- If English content exists → returns English
- If English empty but Uzbek exists → returns Uzbek
- Ensures frontend never receives null/empty posts

#### Video File Support
- Added `video_file` field to serializers
- Returns absolute URLs for both `video_url` and `video_file`

### 4. View Updates (`apps/posts/views.py`)

#### Search Enhancement
- Search now queries across ALL language fields
- Single search query finds posts regardless of language

### 5. File Upload Utilities

#### New Function (`apps/common/utils/files/files.py`)
- Added `unique_video_path()` function
- Generates unique filenames with timestamps
- Stores in `post_videos/` directory

## Usage Guide

### For Frontend Developers

#### Requesting Posts in Specific Language
```javascript
// Get posts in Russian
fetch('/api/posts/?lang=ru')

// Get posts in English
fetch('/api/posts/latest-news/?lang=en')

// Get posts in Uzbek (default)
fetch('/api/posts/')
```

#### Response Structure
```json
{
  "id": 1,
  "title": "Sarlavha",  // Returns in requested language with fallback
  "slug": "sarlavha",
  "short_description": "Qisqacha tavsif",
  "content": "To'liq mazmun",
  "image": "http://example.com/media/post_images/image.jpg",
  "video_url": "https://youtube.com/watch?v=...",  // OR
  "video_file": "http://example.com/media/post_videos/video.mp4",  // One or the other
  "category": {...},
  "published_at": "2026-01-18T10:00:00Z",
  "views_count": 150
}
```

#### Key Points for Frontend
1. **Always check both `video_url` and `video_file`** - only one will be present
2. **Language fallback is automatic** - you always get content even if translation missing
3. **Use `lang` parameter** to request specific language
4. **Search works across all languages** - no need to specify language for search

### For Admin Users

#### Creating a Post

1. **Uzbek Section (Required)**
   - Enter at least `title_uz` (required)
   - Add `short_description_uz` and `content_uz` as needed

2. **Russian/English Sections (Optional)**
   - Expand sections if you want to add translations
   - Leave empty if translation not available

3. **Media Section**
   - Upload an image for thumbnail
   - For videos:
     - **Option A:** Enter YouTube/external URL in `video_url`
     - **Option B:** Upload video file in `video_file`
     - **DO NOT use both** - system will reject it

4. **Publishing**
   - Set status to "Published"
   - Set publication date

#### Validation Rules
- ✅ Can have only Uzbek content (other languages empty)
- ✅ Can use video URL without file
- ✅ Can upload video file without URL
- ❌ Cannot use both video URL and file simultaneously
- ✅ If only Uzbek content exists, all languages will show Uzbek in API

## Testing Checklist

### Video Upload Tests
- [x] Upload video file only → Works
- [x] Enter video URL only → Works
- [x] Try both URL and file → Validation error (as expected)
- [x] Video file URL returned in API → Works

### Multi-Language Tests
- [x] Post with only Uzbek → All languages return Uzbek
- [x] Post with Uzbek + Russian → Russian request gets Russian, English gets Uzbek
- [x] API without lang parameter → Returns Uzbek (default)
- [x] Search across languages → Finds posts in any language
- [x] Admin panel display → Shows Uzbek title or first available

### Edge Cases
- [x] Empty translations → Fallback works
- [x] Unicode in Uzbek text → Slug generation works
- [x] Backward compatibility → Old `post.title` property works

## Migration Applied

Migration file: `apps/posts/migrations/0002_remove_post_content_remove_post_short_description_and_more.py`

Changes:
- Removed old single-language fields
- Added multi-language fields (uz, ru, en)
- Added video_file field
- Updated video_url field help text

## File Structure Changes

```
apps/
  common/
    utils/
      files/
        files.py  # Added unique_video_path()
  posts/
    models/
      post.py  # Updated with multi-language fields and video_file
    serializers/
      post.py  # Updated with language support and fallback logic
    admin.py  # Reorganized for multi-language sections
    views.py  # Updated search to work across languages
```

## Environment Configuration

No additional environment variables needed. Uses existing storage configuration:
- `USE_S3_STORAGE` - If True, stores videos in S3; if False, stores locally in `media/post_videos/`

## Performance Considerations

1. **Database Queries** - No additional queries added; same join patterns
2. **Search Performance** - Searches across more fields but uses database indexes
3. **File Storage** - Videos stored efficiently with unique filenames and timestamps

## Future Enhancements (Optional)

1. Add language-specific slugs (slug_uz, slug_ru, slug_en)
2. Add automatic translation integration (e.g., Google Translate API)
3. Add language-specific SEO meta fields
4. Add video transcoding for different quality levels
5. Add subtitle support for videos

## Support

For questions or issues:
1. Check validation errors in admin panel
2. Test API with different `lang` parameters
3. Verify video file/URL exclusivity
4. Ensure at least Uzbek content is provided

---

**Implementation Date:** January 18, 2026
**Django Version:** 6.0.1
**Python Version:** 3.14.2
