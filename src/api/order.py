from datetime import datetime
from typing import (
    Optional,
    List,
    Literal,
)


from fastapi import APIRouter, Depends, Query

from src.schemas.pagination import Paginated
from src.schemas.order import OrderIn, OrderOut

from src.lib import retailcrm

from src.lib.send_request import HttpxClient, client_dependency, build_params


api = APIRouter()


@api.get("/list", response_model=Paginated[OrderOut])
async def get_all_orders_by_customer_id_paginated(
    http_client: HttpxClient = Depends(client_dependency),
    customer_id: int = Query(description="Reltaed cusotmer id"),
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
    return await retailcrm.fetch_orders_page_by_customer_id(
        http_client,
        int(pagination_limit),
        pagination_offset,
        customer_id,
    )


@api.get("/list/all", response_model=List[OrderOut])
async def get_all_orders_by_customer_id(
    http_client: HttpxClient = Depends(client_dependency),
    customer_id: int = Query(description="Reltaed cusotmer id"),
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
    """
    Retrieve **all** orders, **bypassing** pagination
    """
    all_orders = list()
    limit = 100
    offset = 0
    while True:
        page = await retailcrm.fetch_orders_page_by_customer_id(
            http_client,
            int(pagination_limit),
            pagination_offset,
            customer_id,
        )
        all_orders.extend(page.data)
        if page.total <= page.limit + page.offset:
            break
        offset += limit

    return all_orders


@api.post("/")
async def create_order(
    order: OrderIn,
    http_client: HttpxClient = Depends(client_dependency),
):
    await retailcrm.post_order(http_client, order)
    return {"details": "created"}
