import uuid

from django.db import models
from taggit.managers import TaggableManager


class Bookmark(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.URLField("Resource URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)
