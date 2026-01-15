from rest_framework import serializers
from apps.posts.models import Post, PostCategory


class PostCategorySerializer(serializers.ModelSerializer):
    """Serializer for post categories"""
    class Meta:
        model = PostCategory
        fields = ["id", "name", "type", "description"]


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list view of posts"""
    category = PostCategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

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
            "type_tag",
            "published_at",
            "created_at",
            "views_count",
        ]

    def get_image(self, obj):
        """Return full URL for image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail view of posts"""
    category = PostCategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

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
            "type_tag",
            "status",
            "published_at",
            "created_at",
            "updated_at",
            "views_count",
        ]

    def get_image(self, obj):
        """Return full URL for image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

