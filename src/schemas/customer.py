from typing import List, Any, Dict, Optional


from pydantic import BaseModel, Field
from datetime import datetime

from src.lib.serializer import serialize_time


class CustomerOut(BaseModel):
    type: str = Field(..., description="Customer type")
    id: int = Field(..., description="Customer ID")
    isContact: Optional[bool] = Field(None, description="Whether the customer is a contact person")
    createdAt: Optional[str] = Field(None, description="Customer creation date")
    vip: Optional[bool] = Field(None, description="VIP client")
    bad: Optional[bool] = Field(None, description="Bad client")
    site: Optional[str] = Field(None, description="Store symbolic code")
    tags: Optional[List[Any]] = Field(None, description="List of tags")
    customFields: Optional[List[Any]] = Field(None, description="List of custom fields")
    personalDiscount: Optional[float] = Field(None, description="Personal discount value")
    marginSumm: Optional[float] = Field(None, description="Margin sum")
    totalSumm: Optional[float] = Field(None, description="Total sum")
    averageSumm: Optional[float] = Field(None, description="Average sum")
    ordersCount: Optional[int] = Field(None, description="Total number of orders")
    address: Optional[Dict[str, Any]] = Field(None, description="Customer address data")
    segments: Optional[List[Any]] = Field(None, description="Customer segments")
    firstName: str = Field(..., description="Customer first name")
    lastName: Optional[str] = Field(None, description="Customer last name")
    email: Optional[str] = Field(None, description="Customer email")
    customerSubscriptions: Optional[List[Dict[str, Any]]] = Field(None, description="List of customer subscriptions")
    phones: Optional[List[Any]] = Field(None, description="List of phone numbers")
    mgCustomers: Optional[List[Any]] = Field(None, description="List of MessageGateway customers")


class CustomerContragent(BaseModel):
    contragentType: Optional[str] = Field(None, description="Type of the contragent")
    legalName: Optional[str] = Field(None, description="Full legal name")
    legalAddress: Optional[str] = Field(None, description="Registered address")
    INN: Optional[str] = Field(None, description="Taxpayer Identification Number")
    OKPO: Optional[str] = Field(None, description="OKPO code")
    KPP: Optional[str] = Field(None, description="KPP code")
    OGRN: Optional[str] = Field(None, description="OGRN number")
    OGRNIP: Optional[str] = Field(None, description="OGRNIP number")
    certificateNumber: Optional[str] = Field(None, description="Certificate number")
    certificateDate: Optional[datetime] = Field(None, description="Certificate date")
    BIK: Optional[str] = Field(None, description="Bank Identification Code")
    bank: Optional[str] = Field(None, description="Bank name")
    bankAddress: Optional[str] = Field(None, description="Bank address")
    corrAccount: Optional[str] = Field(None, description="Correspondent account")
    bankAccount: Optional[str] = Field(None, description="Bank account number")

    class Config:
        json_encoders = {
            datetime: serialize_time
        }


class CustomerAddress(BaseModel):
    index: Optional[str] = Field(None, description="Postal index / ZIP code")
    countryIso: Optional[str] = Field(None, description="Country ISO code")
    region: Optional[str] = Field(None, description="Region / state")
    regionId: Optional[int] = Field(None, description="Region ID in Geohelper")
    city: Optional[str] = Field(None, description="City")
    cityId: Optional[int] = Field(None, description="City ID in Geohelper")
    cityType: Optional[str] = Field(None, description="City type")
    street: Optional[str] = Field(None, description="Street name")
    streetId: Optional[int] = Field(None, description="Street ID in Geohelper")
    streetType: Optional[str] = Field(None, description="Street type")
    building: Optional[str] = Field(None, description="Building number")
    flat: Optional[str] = Field(None, description="Apartment / office number")
    floor: Optional[int] = Field(None, description="Floor")
    block: Optional[int] = Field(None, description="Entrance / block")
    house: Optional[str] = Field(None, description="House / structure")
    housing: Optional[str] = Field(None, description="Housing / building section")
    metro: Optional[str] = Field(None, description="Nearest metro station")
    notes: Optional[str] = Field(None, description="Notes about the address")
    text: Optional[str] = Field(None, description="Full address as text")


class CustomerPhone(BaseModel):
    number: str = Field(..., description="Phone number")


class SerializedSource(BaseModel):
    source: Optional[str] = Field(None, description="Source of the client")
    medium: Optional[str] = Field(None, description="Marketing medium / channel")
    campaign: Optional[str] = Field(None, description="Campaign name")
    keyword: Optional[str] = Field(None, description="Campaign keyword")
    content: Optional[str] = Field(None, description="Campaign content")


class MGCustomer(BaseModel):
    mg_id: Optional[str] = Field(None, description="MessageGateway customer ID")


class SerializedCustomer(BaseModel):
    externalId: Optional[str] = Field(None, description="External client ID")
    is_contact: Optional[bool] = Field(False, description="Whether the client is a contact person")
    createdAt: Optional[datetime] = Field(None, description="Client creation date")
    vip: Optional[bool] = Field(False, description="VIP client")
    bad: Optional[bool] = Field(False, description="Bad client")
    contragent: Optional[CustomerContragent] = Field(None, description="Contragent details")
    customFields: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom fields")
    personalDiscount: Optional[float] = Field(0.0, description="Personal discount")
    discountCardNumber: Optional[str] = Field(None, description="Discount card number")
    address: Optional[CustomerAddress] = Field(None, description="Client address")
    firstName: Optional[str] = Field(None, description="First name")
    lastName: Optional[str] = Field(None, description="Last name")
    patronymic: Optional[str] = Field(None, description="Middle name / patronymic")
    email: Optional[str] = Field(None, description="Email address")
    phones: Optional[List[CustomerPhone]] = Field(default_factory=list, description="Phone numbers")
    birthday: Optional[datetime] = Field(None, description="Birthday")
    photoUrl: Optional[str] = Field(None, description="Photo URL")
    managerId: Optional[int] = Field(None, description="Client manager ID")
    sex: Optional[str] = Field(None, description="Gender")
    source: Optional[SerializedSource] = Field(None, description="Client source")
    mgCustomerId: Optional[MGCustomer] = Field(None, description="MessageGateway client ID")
    subscribed: Optional[bool] = Field(True, description="Email subscription status")
    tags: Optional[List[str]] = Field(default_factory=list, description="Client tags")
    attachedTag: Optional[str] = Field(None, description="Attached tag")
    browserId: Optional[str] = Field(None, description="Browser / session ID")

    class Config:
        json_encoders = {
            datetime: serialize_time
        }


class CustomerIn(BaseModel):
    customer: SerializedCustomer = Field(..., description="Client details")

    class Config:
        json_encoders = {
            datetime: serialize_time
        }
