from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required"""
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authorzed user tags"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testuser@gmail.com", "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retriving tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tag returned are for auth user"""
        user2 = get_user_model().objects.create_user("testuser2@gmail.com", "testpass2")
        tag = Tag.objects.create(user=self.user, name="Fast Food")
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tags_successful(self):
        """Test create new tag"""
        payload = {"name": "Test Tag"}
        self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload.get("name")).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test create new tag with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
