from decimal import Decimal

from rest_framework import serializers

from .models import Transaction


class PaymentSerializer(serializers.Serializer):

    card_id = serializers.IntegerField()

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    simulate_result = serializers.ChoiceField(
        choices=["SUCCESS", "FAILED"],
        required=False,
        default="SUCCESS"
    )

    def validate_amount(self, value):

        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "Amount must be greater than 0."
            )

        return value


class TransactionSerializer(serializers.ModelSerializer):

    card_number = serializers.CharField(
        source="card.last_four_digits",
        read_only=True
    )

    class Meta:

        model = Transaction

        fields = [
            "transaction_id",
            "card_number",
            "amount",
            "status",
            "failure_reason",
            "created_at",
            "completed_at",
        ]