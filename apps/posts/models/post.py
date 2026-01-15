from django.db import IntegrityError, models
from decouple import config

from apps.common.models import BaseModel
from apps.common.utils.files import unique_image_path
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

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True
    )

    short_description = models.TextField(blank=True, help_text="Brief description or excerpt")
    content = models.TextField(blank=True, help_text="Main content of the post")

    # For image/video posts
    image = models.ImageField(
        upload_to=unique_image_path,
        null=True,
        blank=True,
        help_text="Featured image or thumbnail"
    )

    # For video posts
    video_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="YouTube or external video URL"
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.__class__, self.title, allow_unicode=True)
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            if not self.slug:
                self.slug = generate_unique_slug(self.__class__, self.title, allow_unicode=True)
                return super().save(*args, **kwargs)
            raise

    def __str__(self):
        return self.title

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

