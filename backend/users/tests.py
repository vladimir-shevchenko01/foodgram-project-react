from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import CustomUser, Subscribe
from .views import UserViewSet


class TestUserViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mixer.blend(CustomUser)

    def test_me(self):
        request = self.factory.get('api/me/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'me'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_subscribe(self):
        author = mixer.blend(CustomUser)
        request = self.factory.post(f'api/users/{author.id}/subscribe/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'post': 'subscribe'})
        response = view(request, pk=author.id)
        self.assertEqual(response.status_code, 201)

    def test_unsubscribe(self):
        author = mixer.blend(CustomUser)
        Subscribe.objects.create(user=self.user, author=author)
        request = self.factory.delete(f'api/users/{author.id}/subscribe/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'delete': 'subscribe'})
        response = view(request, pk=author.id)
        self.assertEqual(response.status_code, 204)

    def test_subscriptions(self):
        request = self.factory.get('api/subscribe/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'subscriptions'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
