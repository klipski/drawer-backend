from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from drawer.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Bookmark
        fields = ['created_at', 'deleted', 'uid', 'updated_at', 'url', 'tags']
