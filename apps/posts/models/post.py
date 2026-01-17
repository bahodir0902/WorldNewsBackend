from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from decouple import config

from apps.common.models import BaseModel
from apps.common.utils.files import unique_image_path, unique_video_path
from apps.common.utils.utils import generate_unique_slug


class PostCategory(BaseModel):
    """Categories for posts (News, Announcements, Reports, Media)"""
    class CategoryType(models.TextChoices):
        NEWS = "news", "News"
        ANNOUNCEMENT = "announcement", "Official Announcement"
        REPORT = "report", "Report"
        MEDIA = "media", "Media/Video"

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=CategoryType.choices)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "PostCategories"
        verbose_name = "Post Category"
        verbose_name_plural = "Post Categories"
        ordering = ["name"]


class Post(BaseModel):
    """Main post model for all types of content"""
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    # Multi-language support - Uzbek (main), Russian, English
    title_uz = models.CharField(max_length=255, verbose_name="Title (Uzbek)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (Russian)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (English)")
    
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True
    )

    short_description_uz = models.TextField(blank=True, help_text="Brief description (Uzbek)")
    short_description_ru = models.TextField(blank=True, help_text="Brief description (Russian)")
    short_description_en = models.TextField(blank=True, help_text="Brief description (English)")
    
    content_uz = models.TextField(blank=True, help_text="Main content (Uzbek)")
    content_ru = models.TextField(blank=True, help_text="Main content (Russian)")
    content_en = models.TextField(blank=True, help_text="Main content (English)")

    # For image/video posts
    image = models.ImageField(
        upload_to=unique_image_path,
        null=True,
        blank=True,
        help_text="Featured image or thumbnail"
    )

    # For video posts - URL or file upload (mutually exclusive)
    video_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="YouTube or external video URL (use either URL or file, not both)"
    )
    
    video_file = models.FileField(
        upload_to=unique_video_path,
        null=True,
        blank=True,
        help_text="Upload video file (use either URL or file, not both)"
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    # For better categorization
    type_tag = models.CharField(
        max_length=50,
        blank=True,
        help_text="Additional type tag (e.g., 'Education', 'Technology')"
    )

    # Views tracking
    views_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["category", "status"]),
            models.Index(fields=["slug"]),
        ]
        db_table = "Posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def clean(self):
        """Validate that video_file and video_url are not both provided"""
        super().clean()
        if self.video_file and self.video_url:
            raise ValidationError({
                'video_file': 'Cannot provide both video file and video URL. Please use only one.',
                'video_url': 'Cannot provide both video file and video URL. Please use only one.',
            })

    def save(self, *args, **kwargs):
        # Run full validation including clean()
        self.full_clean()
        
        if not self.slug:
            # Use Uzbek title for slug generation (main language)
            self.slug = generate_unique_slug(self.__class__, self.title_uz, allow_unicode=True)
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            if not self.slug:
                self.slug = generate_unique_slug(self.__class__, self.title_uz, allow_unicode=True)
                return super().save(*args, **kwargs)
            raise

    def __str__(self):
        return self.title_uz

    @property
    def title(self):
        """Backward compatibility - returns Uzbek title"""
        return self.title_uz
    
    @property
    def short_description(self):
        """Backward compatibility - returns Uzbek short description"""
        return self.short_description_uz
    
    @property
    def content(self):
        """Backward compatibility - returns Uzbek content"""
        return self.content_uz

    @property
    def image_url(self):
        """Get the full URL for the image"""
        if self.image:
            # Check if using S3
            use_s3 = config('USE_S3_STORAGE', default=False, cast=bool)
            if use_s3:
                return self.image.url
            else:
                return self.image.url
        return None
    
    @property
    def video_file_url(self):
        """Get the full URL for the video file"""
        if self.video_file:
            # Check if using S3
            use_s3 = config('USE_S3_STORAGE', default=False, cast=bool)
            if use_s3:
                return self.video_file.url
            else:
                return self.video_file.url
        return None

