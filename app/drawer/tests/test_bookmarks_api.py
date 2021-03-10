from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from drawer.models import Bookmark
from drawer.serializers import BookmarkSerializer

User = get_user_model()
BOOKMARKS_API = 'bookmarks'


class TestBookmarksAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='top_secret123')
        cls.user2 = User.objects.create(username='user2', password='***super_secret***')
        Bookmark.objects.create(url='https://www.djangoproject.com/', drawer=cls.user1.drawer)
        Bookmark.objects.create(url='https://www.django-rest-framework.org/', drawer=cls.user1.drawer)
        Bookmark.objects.create(url='http://localhost:8000/', drawer=cls.user2.drawer)

    def test_list_by_not_authenticated_user(self):
        res = self.client.get(reverse(f'{BOOKMARKS_API}-list'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_by_not_authenticated_user(self):
        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.post(reverse(f'{BOOKMARKS_API}-list'), data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_by_not_authenticated_user(self):
        bookmark = Bookmark.objects.first()
        res = self.client.get(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_not_authenticated_user(self):
        bookmark = Bookmark.objects.first()
        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.put(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}), data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_by_not_authenticated_user(self):
        bookmark = Bookmark.objects.first()
        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.patch(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}), data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_by_not_authenticated_user(self):
        bookmark = Bookmark.objects.first()
        res = self.client.delete(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        self.client.force_authenticate(self.user1)

        res = self.client.get(reverse(f'{BOOKMARKS_API}-list'))
        serialized = BookmarkSerializer(self.user1.drawer.bookmarks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_create(self):
        self.client.force_authenticate(self.user1)

        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.post(reverse(f'{BOOKMARKS_API}-list'), data=payload)
        bookmark = Bookmark.objects.order_by('created_at').last()
        serialized = BookmarkSerializer(bookmark)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serialized.data)

    def test_retrieve(self):
        self.client.force_authenticate(self.user1)

        bookmark = self.user1.drawer.bookmarks.first()

        res = self.client.get(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}))
        serialized = BookmarkSerializer(bookmark)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_update(self):
        self.client.force_authenticate(self.user1)

        bookmark = self.user1.drawer.bookmarks.first()
        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.put(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}), data=payload)
        bookmark.refresh_from_db()
        serialized = BookmarkSerializer(bookmark)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_partial_update(self):
        self.client.force_authenticate(self.user1)

        bookmark = self.user1.drawer.bookmarks.first()
        payload = {
            'url': 'https://en.wikipedia.org/wiki/Main_Page'
        }
        res = self.client.patch(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}), data=payload)
        bookmark.refresh_from_db()
        serialized = BookmarkSerializer(bookmark)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_delete(self):
        self.client.force_authenticate(self.user1)

        bookmark = self.user1.drawer.bookmarks.first()
        res = self.client.delete(reverse(f'{BOOKMARKS_API}-detail', kwargs={'uid': bookmark.uid}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Bookmark.objects.filter(uid=bookmark.uid).exists())
