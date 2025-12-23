from typing import List, Any, Dict, Optional


from pydantic import BaseModel, Field
from datetime import datetime

from src.lib.serializer import serialize_time


class SerializedRelationCustomer(BaseModel):
    id: Optional[int] = Field(None, description="Internal customer ID")
    externalId: Optional[str] = Field(None, description="External customer ID")
    browserId: Optional[str] = Field(None, description="Collector device ID")
    site: Optional[str] = Field(None, description="Store code, required when passing externalId")
    type: Optional[str] = Field(None, description="Customer type (new customer creation)")
    nickName: Optional[str] = Field(None, description="Corporate client name (for new corporate customer)")


class SerializedOrderProductOffer(BaseModel):
    id: Optional[int] = Field(None, description="Offer ID")
    externalId: Optional[str] = Field(None, description="Offer external ID")
    xmlId: Optional[str] = Field(None, description="Offer XML ID in warehouse system")


class PriceType(BaseModel):
    code: Optional[str] = Field(None, description="Price type code")


class CodeValueModel(BaseModel):
    code: str = Field(..., description="Code")
    value: str = Field(..., description="Value")


class SerializedOrderProductProperty(BaseModel):
    code: Optional[str] = Field(None, description="Property code")
    name: str = Field(..., description="Property name")
    value: str = Field(..., description="Property value")


class SerializedOrderProduct(BaseModel):
    markingCodes: Optional[List[str]] = Field(default_factory=list, description="Marking codes")
    initialPrice: Optional[float] = Field(None, description="Product unit price")
    discountManualAmount: Optional[float] = Field(None, description="Manual discount amount per unit")
    discountManualPercent: Optional[float] = Field(None, description="Manual discount percent per unit")
    vatRate: Optional[str] = Field(None, description="VAT rate")
    createdAt: Optional[datetime] = Field(None, description="Product creation datetime")
    quantity: Optional[float] = Field(None, description="Quantity")
    comment: Optional[str] = Field(None, description="Product comment")
    properties: Optional[List[SerializedOrderProductProperty]] = Field(default_factory=list, description="Product additional properties")
    purchasePrice: Optional[float] = Field(None, description="Purchase price")
    ordering: Optional[int] = Field(None, description="Ordering")
    offer: Optional[SerializedOrderProductOffer] = Field(None, description="Offer details")
    productName: Optional[str] = Field(None, description="Product name")
    status: Optional[str] = Field(None, description="Product status")
    priceType: Optional[PriceType] = Field(None, description="Price type")
    externalId: Optional[str] = Field(None, description="Deprecated external ID")
    externalIds: Optional[List[CodeValueModel]] = Field(default_factory=list, description="External identifiers")

    class Config:
        json_encoders = {
            datetime: serialize_time
        }


class OrderIn(BaseModel):
    customer: Optional[SerializedRelationCustomer] = Field(None, description="Customer details")
    items: Optional[List[SerializedOrderProduct]] = Field(default_factory=list, description="Order items")
    number: str = Field(..., description="Order number")


class OrderOut(BaseModel):
    slug: Optional[Any] = Field(None, description="Deprecated symbolic code")
    bonusesCreditTotal: Optional[float] = Field(None, description="Total credited bonuses")
    bonusesChargeTotal: Optional[float] = Field(None, description="Total charged bonuses")
    summ: Optional[float] = Field(None, description="Sum of products or services")
    currency: Optional[str] = Field(None, description="Order currency")

    id: Optional[int] = Field(None, description="Order ID")
    number: Optional[str] = Field(None, description="Order number")
    externalId: Optional[str] = Field(None, description="External order ID")

    orderType: Optional[str] = Field(None, description="Order type")
    orderMethod: Optional[str] = Field(None, description="Order creation method")
    privilegeType: Optional[str] = Field(None, description="Privilege type")

    countryIso: Optional[str] = Field(None, description="Country ISO code")

    createdAt: Optional[datetime] = Field(None, description="Order creation datetime")
    statusUpdatedAt: Optional[datetime] = Field(None, description="Last status update datetime")

    totalSumm: Optional[float] = Field(None, description="Total order amount with discounts")
    prepaySum: Optional[float] = Field(None, description="Prepaid amount")
    purchaseSumm: Optional[float] = Field(None, description="Total purchase cost")

    personalDiscountPercent: Optional[float] = Field(None, description="Personal discount percent")

    loyaltyLevel: Optional[Dict[str, Any]] = Field(None, description="Loyalty level information")
    loyaltyEventDiscount: Optional[Dict[str, Any]] = Field(None, description="Loyalty event discount")

    mark: Optional[int] = Field(None, description="Order rating")
    markDatetime: Optional[datetime] = Field(None, description="Rating datetime")

    lastName: Optional[str] = Field(None, description="Customer last name")
    firstName: Optional[str] = Field(None, description="Customer first name")
    patronymic: Optional[str] = Field(None, description="Customer patronymic")

    phone: Optional[str] = Field(None, description="Phone number")
    additionalPhone: Optional[str] = Field(None, description="Additional phone number")
    email: Optional[str] = Field(None, description="Email address")

    call: Optional[bool] = Field(None, description="Call required flag")
    expired: Optional[bool] = Field(None, description="Order expired flag")

    customerComment: Optional[str] = Field(None, description="Customer comment")
    managerComment: Optional[str] = Field(None, description="Manager comment")
    managerId: Optional[int] = Field(None, description="Assigned manager ID")

    customer: Optional[Dict[str, Any]] = Field(None, description="Customer object")
    contact: Optional[Dict[str, Any]] = Field(None, description="Contact person")

    company: Optional[Dict[str, Any]] = Field(None, description="Company information")
    contragent: Optional[Dict[str, Any]] = Field(None, description="Contragent details")

    delivery: Optional[Dict[str, Any]] = Field(None, description="Delivery information")

    site: Optional[str] = Field(None, description="Store code")
    status: Optional[str] = Field(None, description="Order status")
    statusComment: Optional[str] = Field(None, description="Last status change comment")

    source: Optional[Dict[str, Any]] = Field(None, description="Order source")

    items: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Order items"
    )

    fullPaidAt: Optional[datetime] = Field(None, description="Full payment datetime")

    payments: Optional[Any] = Field(
        None,
        description="Payments"
    )

    fromApi: Optional[bool] = Field(None, description="Order created via API")

    weight: Optional[float] = Field(None, description="Order weight")
    length: Optional[int] = Field(None, description="Order length")
    width: Optional[int] = Field(None, description="Order width")
    height: Optional[int] = Field(None, description="Order height")

    shipmentStore: Optional[str] = Field(None, description="Shipment warehouse")
    shipmentDate: Optional[datetime] = Field(None, description="Shipment date")
    shipped: Optional[bool] = Field(None, description="Shipped flag")

    links: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Order links"
    )

    customFields: Optional[Any] = Field(
        default_factory=None,
        description="Custom fields"
    )

    clientId: Optional[Any] = Field(None, description="Client identifier")
