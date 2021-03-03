from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drawer.models import Bookmark
from drawer.serializers import BookmarkSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing bookmarks.
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uid'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
