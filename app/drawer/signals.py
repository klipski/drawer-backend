import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from drawer.models import Drawer, Bookmark

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    if created:
        obj, drawer_created = Drawer.objects.get_or_create(user=instance)
        if drawer_created:
            logger.info('Drawer created')


@receiver(pre_save, sender=Bookmark)
def bookmark_saved(sender, instance, **kwargs):
    if instance.deleted:
        try:
            bookmark = Bookmark.objects.get(pk=instance.pk)
            if not bookmark.deleted and bookmark.deleted_at == instance.deleted_at:
                logger.info('Bookmark deleted_at updated')
                instance.deleted_at = datetime.now()
        except Bookmark.DoesNotExist:
            if not instance.deleted_at:
                instance.deleted_at = datetime.now()
                logger.info('Bookmark deleted_at updated')
