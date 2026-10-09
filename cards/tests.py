from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from cards.models import Card


User = get_user_model()


class CardManagementTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="carduser",
            email="carduser@example.com",
            password="TestPass@123",
        )
        self.client.force_authenticate(user=self.user)
        self.url = "/api/cards/"

    def test_add_card_stores_only_masked_number(self):
        response = self.client.post(
            self.url,
            {
                "card_type": "CREDIT",
                "card_holder_name": "TEST USER",
                "card_number": "4111111111111111",
                "expiry_month": 12,
                "expiry_year": 2030,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        card = Card.objects.get(user=self.user)

        self.assertEqual(card.last_four_digits, "1111")
        self.assertNotIn(
            "4111111111111111",
            card.masked_card_number,
        )
        self.assertNotIn("cvv", response.data)

    def test_card_list_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )