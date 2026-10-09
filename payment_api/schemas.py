from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):

    card_id: int

    amount: Decimal = Field(
        gt=0,
        decimal_places=2
    )


class PaymentResponse(BaseModel):

    transaction_id: str
    card_id: int
    amount: Decimal
    status: str
    message: str