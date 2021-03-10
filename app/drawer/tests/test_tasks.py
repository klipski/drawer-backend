from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from drawer.models import Bookmark
from drawer.tasks import delete_expired_bookmarks

User = get_user_model()


class TasksTestCase(TestCase):

    def test_delete_expired_bookmarks(self):
        user = User.objects.create(username='user', password='test123')
        b1 = Bookmark.objects.create(url='https://www.djangoproject.com/', drawer=user.drawer)
        b2 = Bookmark.objects.create(url='https://www.djangoproject.com/', drawer=user.drawer)
        Bookmark.objects.create(url='https://www.djangoproject.com/', drawer=user.drawer)

        user.drawer.remove_after_days = 1
        user.drawer.save()

        b1.deleted = True
        b1.deleted_at = datetime.now() - timedelta(days=2)
        b1.save()

        b2.deleted = True
        b2.deleted_at = datetime.now() - timedelta(days=5)
        b2.save()

        delete_expired_bookmarks()

        self.assertEqual(Bookmark.objects.count(), 1)
