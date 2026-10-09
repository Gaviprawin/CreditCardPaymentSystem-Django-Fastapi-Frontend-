import os
import sys
# import random

from fastapi import APIRouter, HTTPException

# Add Django project path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

sys.path.append(BASE_DIR)

# Configure Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django

django.setup()

from cards.models import Card
from transactions.models import Transaction

from payment_api.schemas import (
    PaymentRequest,
    PaymentResponse,
)


router = APIRouter(
    prefix="/api/payments",
    tags=["Payment Processing"]
)


@router.post(
    "/",
    response_model=PaymentResponse
)
def make_payment(payment: PaymentRequest):

    try:
        card = Card.objects.get(
            id=payment.card_id
        )

    except Card.DoesNotExist:

        raise HTTPException(
            status_code=404,
            detail="Card not found."
        )


    if payment.amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero."
        )


    transaction = Transaction.objects.create(

        user=card.user,

        card=card,

        amount=payment.amount,

        status="PENDING"
    )


    # Simulate successful payment

    transaction.status = "SUCCESS"

    transaction.failure_reason = None

    transaction.save()


    return PaymentResponse(

        transaction_id=str(
            transaction.transaction_id
        ),

        card_id=card.id,

        amount=transaction.amount,

        status=transaction.status,

        message="Payment processed successfully."
    )