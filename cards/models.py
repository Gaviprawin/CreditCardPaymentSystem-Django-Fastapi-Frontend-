from django.conf import settings
from django.db import models


class Card(models.Model):

    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

    CARD_TYPE_CHOICES = [
        (CREDIT, "Credit Card"),
        (DEBIT, "Debit Card"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cards"
    )

    card_type = models.CharField(
        max_length=10,
        choices=CARD_TYPE_CHOICES
    )

    card_holder_name = models.CharField(
        max_length=100
    )

    masked_card_number = models.CharField(
        max_length=25
    )

    last_four_digits = models.CharField(
        max_length=4
    )

    expiry_month = models.PositiveSmallIntegerField()

    expiry_year = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.card_type} - {self.masked_card_number}"