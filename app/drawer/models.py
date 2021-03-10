import uuid

from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Drawer(models.Model):
    user = models.OneToOneField(User, related_name='drawer', on_delete=models.CASCADE)
    remove_after_days = models.PositiveSmallIntegerField(default=30)


class Bookmark(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.URLField("Resource URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    drawer = models.ForeignKey(Drawer, related_name='bookmarks', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    tags = TaggableManager(blank=True)
