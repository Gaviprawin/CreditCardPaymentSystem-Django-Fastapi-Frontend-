from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = "/api/accounts/register/"
        self.login_url = "/api/accounts/login/"
        self.profile_url = "/api/accounts/profile/"

    def test_registration_hashes_password(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "TestPass@123",
                "password2": "TestPass@123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(username="testuser")
        self.assertNotEqual(user.password, "TestPass@123")
        self.assertTrue(user.check_password("TestPass@123"))

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser2",
                "email": "testuser2@example.com",
                "password": "TestPass@123",
                "password2": "DifferentPass@123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_returns_jwt(self):
        User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="TestPass@123",
        )

        response = self.client.post(
            self.login_url,
            {
                "username": "loginuser",
                "password": "TestPass@123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )