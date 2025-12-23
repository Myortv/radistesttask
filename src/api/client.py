from datetime import datetime
from typing import (
    Optional,
    List,
    Literal,
)


from fastapi import APIRouter, Depends, Query

from src.schemas.pagination import Paginated
from src.schemas.customer import CustomerOut, CustomerIn

from src.lib import retailcrm

from src.lib.send_request import HttpxClient, client_dependency



api = APIRouter()


@api.get("/list", response_model=Paginated[CustomerOut])
async def get_all_customers_paginated(
    http_client: HttpxClient = Depends(client_dependency),
    customer_name: Optional[str] = Query(None, description="Customer name. Supports partial match."),
    customer_email: Optional[str] = Query(None, description="Customer email. Supports partial match."),
    customer_registration_date: Optional[datetime] = Query(
        None,
        description="Datetime in iso format.",
        example="2008-09-15",
        examples=["2008-09-15", "2025-12-23T01:49:59Z"],
        openapi_examples={
            "2025-12-23T01:49:59": "2025-12-23T01:49:59",
            "2025-12-23": "2025-12-23",
        },
    ),
    pagination_limit: Literal["20", "50", "100"] = Query(
        "20",
        description="Only 20, 50, 100 as only they are supported by retal crm"
    ),
    pagination_offset: Optional[int] = Query(
        0,
        description="Pagination offset. Should be multiplie of pagination_limit. If not, will be rounded down.",
        ge=0,
    ),
):
    return await retailcrm.fetch_customers_page(
        http_client,
        int(pagination_limit),
        pagination_offset,
        customer_name,
        customer_email,
        customer_registration_date,
    )


@api.get("/list/all", response_model=List[CustomerOut])
async def get_all_customers(
    http_client: HttpxClient = Depends(client_dependency),
    customer_name: Optional[str] = Query(None, description="Customer name. Supports partial match."),
    customer_email: Optional[str] = Query(None, description="Customer email. Supports partial match."),
    customer_registration_date: Optional[datetime] = Query(
        None,
        description="Datetime in iso format.",
        example="2008-09-15",
        examples=["2008-09-15", "2025-12-23T01:49:59Z"],
        openapi_examples={
            "2025-12-23T01:49:59": "2025-12-23T01:49:59",
            "2025-12-23": "2025-12-23",
        },
    ),
):
    """
    return all customers, **bypass** pagination
    """
    all_customers = list()
    limit = 100
    offset = 0
    while True:
        page = await retailcrm.fetch_customers_page(
            http_client,
            limit,
            offset,
            customer_name,
            customer_email,
            customer_registration_date,
        )
        all_customers.extend(page.data)
        if page.total <= page.limit + page.offset:
            break
        offset += limit

    return all_customers


@api.post("/")
async def create_customer(
    customer: CustomerIn,
    http_client: HttpxClient = Depends(client_dependency),
):
    await retailcrm.post_customer(http_client, customer)
    return {"details": "created"}
