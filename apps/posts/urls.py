from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet, PostCategoryViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('categories', PostCategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

