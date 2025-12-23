from typing import Optional


from pydantic import BaseModel, Field
from datetime import datetime


class PaymentIn(BaseModel):
    externalId: Optional[str] = Field(None, description="External payment ID")
    amount: float = Field(..., description="Payment amount in the object's currency")
    paidAt: Optional[datetime] = Field(None, description="Payment date and time")
    comment: Optional[str] = Field(None, description="Payment comment")
    type: str = Field("bank-card", description="Payment type")
    status: str = Field(None, description="Payment status")
