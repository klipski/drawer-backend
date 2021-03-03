import uuid

from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Bookmark(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.URLField("Resource URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
