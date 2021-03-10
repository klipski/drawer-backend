from rest_framework import serializers

from drawer.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = ('id', 'drawer', 'deleted_at')
