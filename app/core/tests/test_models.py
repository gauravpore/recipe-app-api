from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "testuser@gmail.com"
        password = "testuserpassword"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for a new user is normaized"""
        email = "testuser@Gmail.com"
        user = get_user_model().objects.create_user(email, "test321")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "123")

    def test_create_new_super_user(self):
        """Test creating Super User"""
        user = get_user_model().objects.create_superuser(
            "supertestuser@gmail.com", "superuser"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
