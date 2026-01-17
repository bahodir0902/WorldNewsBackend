from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.posts.models import Post, PostCategory
from apps.common.logging import AdminLogger, compare_model_fields


class PostCategoryAdmin(ModelAdmin):
    """Enhanced admin for PostCategory with Unfold"""

    list_display = [
        'name',
        'type_badge',
        'post_count',
        'created_at_display',
    ]
    list_filter = [
        'type',
        'created_at',
    ]
    search_fields = ['name', 'description']
    ordering = ['name']
    prepopulated_fields = {}

    fieldsets = (
        ('📌 Basic Information', {
            'fields': ('name', 'type'),
            'description': 'Core category details',
        }),
        ('📝 Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('📊 Statistics', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Metadata and timestamps',
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    @display(
        description='Type',
        ordering='type',
    )
    def type_badge(self, obj):
        """Display type as a colored badge"""
        colors = {
            'news': '#3B82F6',      # Blue
            'announcement': '#10B981',  # Green
            'report': '#8B5CF6',    # Purple
            'media': '#F59E0B',     # Amber
        }
        color = colors.get(obj.type, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 500; font-size: 12px;">{}</span>',
            color,
            obj.get_type_display()
        )

    @display(
        description='Posts',
        ordering='posts__count',
    )
    def post_count(self, obj):
        """Display number of posts in this category"""
        count = obj.posts.filter(status=Post.Status.PUBLISHED).count()
        return format_html(
            '<span style="background-color: #E5E7EB; padding: 4px 12px; '
            'border-radius: 8px; font-weight: 500;">{} posts</span>',
            count
        )

    @display(
        description='Created',
        ordering='created_at',
    )
    def created_at_display(self, obj):
        """Display created date in readable format"""
        return obj.created_at.strftime('%b %d, %Y')

    def save_model(self, request, obj, form, change):
        """Log category changes"""
        if change:
            # Get the old instance
            old_instance = PostCategory.objects.get(pk=obj.pk)
            changes = compare_model_fields(old_instance, obj)
            AdminLogger.log_action(
                action='UPDATED',
                model_name='Category',
                instance=obj,
                user=request.user,
                changes=changes,
            )
        else:
            AdminLogger.log_action(
                action='CREATED',
                model_name='Category',
                instance=obj,
                user=request.user,
            )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Log category deletion"""
        AdminLogger.log_action(
            action='DELETED',
            model_name='Category',
            instance=obj,
            user=request.user,
        )
        super().delete_model(request, obj)


class PostAdmin(ModelAdmin):
    """Enhanced admin for Post with Unfold and beautiful UI"""

    list_display = [
        'title_preview',
        'category_badge',
        'status_badge',
        'views_count_display',
        'published_date',
        'post_actions',
    ]

    list_filter = [
        'status',
        'category',
        'type_tag',
        'published_at',
        'created_at',
        'views_count',
    ]

    search_fields = ['title_uz', 'title_ru', 'title_en', 'short_description_uz', 'short_description_ru', 'short_description_en', 'content_uz', 'content_ru', 'content_en', 'slug']
    prepopulated_fields = {'slug': ('title_uz',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']

    fieldsets = (
        ('📝 Content - Uzbek (Main)', {
            'fields': ('title_uz', 'slug', 'short_description_uz', 'content_uz'),
            'description': 'Uzbek language content (primary)',
        }),
        ('🇷🇺 Content - Russian', {
            'fields': ('title_ru', 'short_description_ru', 'content_ru'),
            'classes': ('collapse',),
            'description': 'Russian language content (optional)',
        }),
        ('🇬🇧 Content - English', {
            'fields': ('title_en', 'short_description_en', 'content_en'),
            'classes': ('collapse',),
            'description': 'English language content (optional)',
        }),
        ('📌 Categorization', {
            'fields': ('category', 'type_tag'),
            'description': 'Category and tags',
        }),
        ('🖼️ Media', {
            'fields': ('image', 'video_url', 'video_file'),
            'description': 'Images and video content (use either video URL or video file, not both)',
        }),
        ('📊 Publishing', {
            'fields': ('status', 'published_at'),
            'description': 'Visibility and publication settings',
        }),
        ('📈 Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Metadata and view tracking',
        }),
    )

    readonly_fields = ['views_count', 'created_at', 'updated_at',]

    def get_prepopulated_fields(self, request, obj=None):
        """Auto-fill slug from Uzbek title"""
        return {'slug': ('title_uz',)} if not obj else {}

    @display(
        description='Title',
        ordering='title_uz',
    )
    def title_preview(self, obj):
        """Display title with preview"""
        if obj.image:
            image_tag = format_html(
                '<img src="{}" style="width: 40px; height: 40px; '
                'border-radius: 4px; margin-right: 8px; object-fit: cover;" />',
                obj.image.url
            )
        else:
            image_tag = mark_safe(
                '<div style="width: 40px; height: 40px; border-radius: 4px; '
                'margin-right: 8px; background-color: #E5E7EB; '
                'display: flex; align-items: center; justify-content: center; '
                'font-size: 20px;">📄</div>'
            )

        title = obj.title_uz or obj.title_ru or obj.title_en or "Untitled"
        return format_html(
            '{}{}',
            image_tag,
            title[:60] + '...' if len(title) > 60 else title
        )

    @display(
        description='Category',
        ordering='category',
    )
    def category_badge(self, obj):
        """Display category as colored badge"""
        if not obj.category:
            return mark_safe('<span style="color: #6B7280;">Uncategorized</span>')

        colors = {
            'news': '#3B82F6',
            'announcement': '#10B981',
            'report': '#8B5CF6',
            'media': '#F59E0B',
        }
        color = colors.get(obj.category.type, '#6B7280')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 8px; font-size: 12px; font-weight: 500;">{}</span>',
            color,
            obj.category.name
        )

    @display(
        description='Status',
        ordering='status',
    )
    def status_badge(self, obj):
        """Display status as colored badge"""
        status_colors = {
            'draft': '#EF4444',      # Red
            'published': '#10B981',  # Green
        }
        color = status_colors.get(obj.status, '#6B7280')
        emoji = '✓' if obj.status == 'published' else '📝'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 8px; font-size: 12px; font-weight: 500; white-space: nowrap;">'
            '{} {}</span>',
            color,
            emoji,
            obj.get_status_display()
        )

    @display(
        description='Views',
        ordering='views_count',
    )
    def views_count_display(self, obj):
        """Display view count with icon"""
        return format_html(
            '<span style="background-color: #F3F4F6; padding: 4px 8px; '
            'border-radius: 6px; font-weight: 500;">👁️ {}</span>',
            obj.views_count
        )

    @display(
        description='Published',
        ordering='published_at',
    )
    def published_date(self, obj):
        """Display published date"""
        if obj.published_at:
            return obj.published_at.strftime('%b %d, %Y')
        return mark_safe('<span style="color: #9CA3AF;">Not published</span>')

    @display(
        description='Actions',
    )
    def post_actions(self, obj):
        """Quick action buttons"""
        view_url = f'/api/posts/{obj.slug}/'
        return format_html(
            '<a href="{}" style="color: #3B82F6; text-decoration: none; margin-right: 10px;" '
            'title="View on API">🔗 API</a>',
            view_url
        )

    def save_model(self, request, obj, form, change):
        """Log post changes with detailed information"""
        if change:
            # Get the old instance
            old_instance = Post.objects.get(pk=obj.pk)
            changes = compare_model_fields(old_instance, obj)

            extra_info = None
            if 'status' in changes and changes['status'][1] == 'published':
                extra_info = '✨ Post published successfully!'

            AdminLogger.log_action(
                action='UPDATED',
                model_name='Post',
                instance=obj,
                user=request.user,
                changes=changes,
                extra_info=extra_info,
            )
        else:
            AdminLogger.log_action(
                action='CREATED',
                model_name='Post',
                instance=obj,
                user=request.user,
                extra_info='New post created and ready for editing',
            )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Log post deletion"""
        AdminLogger.log_action(
            action='DELETED',
            model_name='Post',
            instance=obj,
            user=request.user,
            extra_info=f'Deleted post: {obj.title}',
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """Log bulk deletion"""
        count = queryset.count()
        AdminLogger.log_bulk_action(
            action='DELETE',
            model_name='Post',
            count=count,
            user=request.user,
            query_description=f'Bulk deleted {count} posts',
        )
        super().delete_queryset(request, queryset)


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
