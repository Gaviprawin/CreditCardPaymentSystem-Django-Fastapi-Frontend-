import re

from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.ModelSerializer):

    card_number = serializers.CharField(
        write_only=True,
        min_length=13,
        max_length=19
    )

    class Meta:
        model = Card

        fields = [
            "id",
            "card_type",
            "card_holder_name",
            "card_number",
            "masked_card_number",
            "last_four_digits",
            "expiry_month",
            "expiry_year",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "masked_card_number",
            "last_four_digits",
            "created_at",
        ]

    def validate_card_number(self, value):

        value = value.replace(" ", "").replace("-", "")

        if not value.isdigit():
            raise serializers.ValidationError(
                "Card number must contain only digits."
            )

        if len(value) < 13 or len(value) > 19:
            raise serializers.ValidationError(
                "Card number must contain 13 to 19 digits."
            )

        return value

    def validate_expiry_month(self, value):

        if value < 1 or value > 12:
            raise serializers.ValidationError(
                "Expiry month must be between 1 and 12."
            )

        return value

    def create(self, validated_data):

        card_number = validated_data.pop("card_number")

        last_four = card_number[-4:]

        masked_number = "*" * (len(card_number) - 4) + last_four

        card = Card.objects.create(
            masked_card_number=masked_number,
            last_four_digits=last_four,
            **validated_data
        )

        return card