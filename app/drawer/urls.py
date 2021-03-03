from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drawer.views import BookmarkViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
