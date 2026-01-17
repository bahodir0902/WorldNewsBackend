from rest_framework import serializers
from apps.posts.models import Post, PostCategory


class PostCategorySerializer(serializers.ModelSerializer):
    """Serializer for post categories"""
    class Meta:
        model = PostCategory
        fields = ["id", "name", "type", "description"]


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list view of posts with multi-language support"""
    category = PostCategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    
    # Language-aware fields
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "short_description",
            "image",
            "video_url",
            "video_file",
            "type_tag",
            "published_at",
            "created_at",
            "views_count",
        ]

    def get_language(self):
        """Get requested language from context, default to 'uz'"""
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang', 'uz').lower()
        return 'uz'

    def get_title(self, obj):
        """Return title in requested language with fallback"""
        lang = self.get_language()
        
        # Try requested language first
        title = getattr(obj, f'title_{lang}', None)
        if title:
            return title
        
        # Fallback chain: uz -> ru -> en
        for fallback_lang in ['uz', 'ru', 'en']:
            title = getattr(obj, f'title_{fallback_lang}', None)
            if title:
                return title
        
        return "Untitled"

    def get_short_description(self, obj):
        """Return short description in requested language with fallback"""
        lang = self.get_language()
        
        # Try requested language first
        desc = getattr(obj, f'short_description_{lang}', None)
        if desc:
            return desc
        
        # Fallback chain: uz -> ru -> en
        for fallback_lang in ['uz', 'ru', 'en']:
            desc = getattr(obj, f'short_description_{fallback_lang}', None)
            if desc:
                return desc
        
        return ""

    def get_image(self, obj):
        """Return full URL for image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_video_file(self, obj):
        """Return full URL for video file"""
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail view of posts with multi-language support"""
    category = PostCategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    
    # Language-aware fields
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "short_description",
            "content",
            "image",
            "video_url",
            "video_file",
            "type_tag",
            "status",
            "published_at",
            "created_at",
            "updated_at",
            "views_count",
        ]

    def get_language(self):
        """Get requested language from context, default to 'uz'"""
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang', 'uz').lower()
        return 'uz'

    def get_title(self, obj):
        """Return title in requested language with fallback"""
        lang = self.get_language()
        
        # Try requested language first
        title = getattr(obj, f'title_{lang}', None)
        if title:
            return title
        
        # Fallback chain: uz -> ru -> en
        for fallback_lang in ['uz', 'ru', 'en']:
            title = getattr(obj, f'title_{fallback_lang}', None)
            if title:
                return title
        
        return "Untitled"

    def get_short_description(self, obj):
        """Return short description in requested language with fallback"""
        lang = self.get_language()
        
        # Try requested language first
        desc = getattr(obj, f'short_description_{lang}', None)
        if desc:
            return desc
        
        # Fallback chain: uz -> ru -> en
        for fallback_lang in ['uz', 'ru', 'en']:
            desc = getattr(obj, f'short_description_{fallback_lang}', None)
            if desc:
                return desc
        
        return ""

    def get_content(self, obj):
        """Return content in requested language with fallback"""
        lang = self.get_language()
        
        # Try requested language first
        content = getattr(obj, f'content_{lang}', None)
        if content:
            return content
        
        # Fallback chain: uz -> ru -> en
        for fallback_lang in ['uz', 'ru', 'en']:
            content = getattr(obj, f'content_{fallback_lang}', None)
            if content:
                return content
        
        return ""

    def get_image(self, obj):
        """Return full URL for image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_video_file(self, obj):
        """Return full URL for video file"""
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return None

