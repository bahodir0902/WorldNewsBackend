from django.db.models import Q, F
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.posts.models import Post, PostCategory
from apps.posts.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCategorySerializer,
)


class PostPagination(PageNumberPagination):
    """Pagination for posts"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for posts (News, Announcements, Media, Reports)
    Provides list, retrieve, and filtered endpoints
    """
    queryset = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).select_related('category').order_by('-published_at', '-created_at')

    serializer_class = PostListSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        """Get single post and increment view count"""
        instance = self.get_object()

        # Increment view count
        Post.objects.filter(pk=instance.pk).update(
            views_count=F('views_count') + 1
        )
        instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='news')
    def news(self, request):
        """Get all news posts"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.NEWS
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='latest-news')
    def latest_news(self, request):
        """Get latest news for homepage"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.NEWS
        )[:15]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='announcements')
    def announcements(self, request):
        """Get all official announcements"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.ANNOUNCEMENT
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='latest-announcements')
    def latest_announcements(self, request):
        """Get latest announcements for homepage"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.ANNOUNCEMENT
        )[:4]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='media')
    def media(self, request):
        """Get all media/video posts"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.MEDIA
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='latest-videos')
    def latest_videos(self, request):
        """Get latest videos for homepage"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.MEDIA
        )[:4]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='reports')
    def reports(self, request):
        """Get all reports"""
        queryset = self.get_queryset().filter(
            category__type=PostCategory.CategoryType.REPORT
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """Search posts by title or description in all languages"""
        query = request.query_params.get('q', '')

        if not query:
            return Response(
                {"detail": "Search query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Search across all language fields
        queryset = self.get_queryset().filter(
            Q(title_uz__icontains=query) |
            Q(title_ru__icontains=query) |
            Q(title_en__icontains=query) |
            Q(short_description_uz__icontains=query) |
            Q(short_description_ru__icontains=query) |
            Q(short_description_en__icontains=query) |
            Q(content_uz__icontains=query) |
            Q(content_ru__icontains=query) |
            Q(content_en__icontains=query)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Categories"])
class PostCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for post categories"""
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None
