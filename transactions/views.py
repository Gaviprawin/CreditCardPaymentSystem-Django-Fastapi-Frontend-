import csv
import random

from django.http import HttpResponse
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q
from datetime import datetime, time, timedelta
from rest_framework.renderers import BaseRenderer

from cards.models import Card

from .models import Transaction
from .serializers import (
    PaymentSerializer,
    TransactionSerializer,
)


class PaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        card_id = serializer.validated_data["card_id"]

        amount = serializer.validated_data["amount"]

        simulate_result = serializer.validated_data.get(
            "simulate_result"
        )

        try:

            card = Card.objects.get(
                id=card_id,
                user=request.user
            )

        except Card.DoesNotExist:

            return Response(
                {
                    "message": "Card not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        transaction = Transaction.objects.create(
            user=request.user,
            card=card,
            amount=amount,
            status=Transaction.PENDING
        )

        # Simulate payment processing
        if simulate_result == "SUCCESS":

            final_status = Transaction.SUCCESS

            failure_reason = None

        elif simulate_result == "FAILED":

            final_status = Transaction.FAILED

            failure_reason = "Payment simulation failed."

        else:

            final_status = random.choice(
                [
                    Transaction.SUCCESS,
                    Transaction.FAILED
                ]
            )

            failure_reason = (
                "Payment simulation failed."
                if final_status == Transaction.FAILED
                else None
            )

        transaction.status = final_status

        transaction.failure_reason = failure_reason

        transaction.completed_at = timezone.now()

        transaction.save()

        return Response(
            {
                "message": "Payment processed.",
                "transaction_id": transaction.transaction_id,
                "amount": transaction.amount,
                "status": transaction.status,
            },
            status=status.HTTP_201_CREATED
        )


class TransactionListView(generics.ListAPIView):

    serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Transaction.objects.filter(
            user=self.request.user
        )

        status_value = self.request.query_params.get(
            "status"
        )

        min_amount = self.request.query_params.get(
            "min_amount"
        )

        max_amount = self.request.query_params.get(
            "max_amount"
        )

        date_from = self.request.query_params.get(
            "date_from"
        )

        date_to = self.request.query_params.get(
            "date_to"
        )

        if status_value:

            queryset = queryset.filter(
                status=status_value.upper()
            )

        if min_amount:

            queryset = queryset.filter(
                amount__gte=min_amount
            )

        if max_amount:

            queryset = queryset.filter(
                amount__lte=max_amount
            )

        if date_from:

            queryset = queryset.filter(
                created_at__date__gte=date_from
            )

        if date_to:

            queryset = queryset.filter(
                created_at__date__lte=date_to
            )

        return queryset


class TransactionDetailView(generics.RetrieveAPIView):

    serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Transaction.objects.filter(
            user=self.request.user
        )


class CSVRenderer(BaseRenderer):
    media_type = "text/csv"
    format = "csv"
    charset = "utf-8"
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class AdminTransactionExportView(APIView):

    permission_classes = [IsAdminUser]
    renderer_classes = [CSVRenderer]

    def get(self, request):

        transactions = Transaction.objects.select_related(
            "user",
            "card"
        ).all()

        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            'attachment; filename="transactions.csv"'
        )

        writer = csv.writer(response)

        writer.writerow(
            [
                "Transaction ID",
                "Username",
                "Card Last 4",
                "Amount",
                "Status",
                "Created At",
                "Completed At",
            ]
        )

        for transaction in transactions:

            writer.writerow(
                [
                    transaction.transaction_id,
                    transaction.user.username,
                    (
                        transaction.card.last_four_digits
                        if transaction.card
                        else ""
                    ),
                    transaction.amount,
                    transaction.status,
                    transaction.created_at,
                    transaction.completed_at,
                ]
            )

        return response


class AdminDailySummaryView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        today = timezone.localdate()

        start = timezone.make_aware(
            datetime.combine(today, time.min)
        )

        end = timezone.make_aware(
            datetime.combine(
                today + timedelta(days=1),
                time.min
            )
        )

        daily_transactions = Transaction.objects.filter(
            created_at__gte=start,
            created_at__lt=end,
        )

        summary = daily_transactions.aggregate(
            total_transactions=Count("id"),
            successful_payments=Count(
                "id",
                filter=Q(status="SUCCESS"),
            ),
            failed_payments=Count(
                "id",
                filter=Q(status="FAILED"),
            ),
            pending_payments=Count(
                "id",
                filter=Q(status="PENDING"),
            ),
            total_payment_amount=Sum("amount"),
        )

        return Response({
            "date": today.isoformat(),
            "total_transactions": (
                summary["total_transactions"] or 0
            ),
            "successful_payments": (
                summary["successful_payments"] or 0
            ),
            "failed_payments": (
                summary["failed_payments"] or 0
            ),
            "pending_payments": (
                summary["pending_payments"] or 0
            ),
            "total_payment_amount": str(
                summary["total_payment_amount"] or 0
            ),
        })