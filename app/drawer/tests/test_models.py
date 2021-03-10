from django.contrib.auth import get_user_model
from django.test import TestCase
from drawer.models import Bookmark, Drawer

User = get_user_model()


class DrawerTestCase(TestCase):

    def test_drawer_created_after_user_is_created(self):
        self.assertEqual(Drawer.objects.count(), 0)

        user = User.objects.create(username='john', password='butterfly')

        self.assertIsInstance(user.drawer, Drawer)
        self.assertEqual(Drawer.objects.count(), 1)


class BookmarkTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1', password='top_secret123')
        Bookmark.objects.create(url='https://www.djangoproject.com/', drawer=cls.user.drawer)
        Bookmark.objects.create(url='https://www.django-rest-framework.org/', drawer=cls.user.drawer)

    def test_deleted_at_update_after_changed_deleted_attribute(self):
        bookmark = Bookmark.objects.first()
        self.assertFalse(bookmark.deleted)
        self.assertIsNone(bookmark.deleted_at)

        bookmark.deleted = True
        bookmark.save()
        bookmark.refresh_from_db()

        self.assertIsNotNone(bookmark.deleted_at)

    def test_deleted_at_update_after_create_bookmark_with_deleted_attribute(self):
        bookmark = Bookmark.objects.create(url='https://localhost:8080/', drawer=self.user.drawer, deleted=True)

        self.assertIsNotNone(bookmark.deleted_at)
