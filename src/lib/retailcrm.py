import json

from datetime import datetime
from typing import (
    Optional,
)


from src.schemas.pagination import Paginated
from src.schemas.customer import CustomerOut, CustomerIn
from src.schemas.order import OrderIn, OrderOut
from src.schemas.payment import PaymentIn

from src.lib.send_request import HttpxClient, build_params

from src.core.configs import configs


async def fetch_customers_page(
    http_client: HttpxClient,
    pagination_limit: int,
    pagination_offset: int,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    customer_registration_date: Optional[datetime] = None,
) -> Paginated[CustomerOut]:
    params = build_params(
        {
            "filter[name]": customer_name,
            "filter[email]": customer_email,
            "filter[dateFrom]": customer_registration_date,
            "filter[dateTo]": customer_registration_date,
        },
        limit=pagination_limit,
        page=int(pagination_offset/pagination_limit) + 1
    )

    json_response = await http_client.request(
        "GET",
        f"{configs.RETAIL_CRM_HOST}/api/v5/customers",
        params=params,
    )
    return Paginated(
        limit=json_response['pagination']['limit'],
        offset=json_response['pagination']['limit'] * (json_response['pagination']['currentPage'] - 1),
        total=json_response['pagination']['totalCount'],
        data=[CustomerOut(**customer) for customer in json_response['customers']]
    )


async def post_customer(
    http_client: HttpxClient,
    customer: CustomerIn
):
    await http_client.request(
        "POST",
        f"{configs.RETAIL_CRM_HOST}/api/v5/customers/create",
        data={
            "customer": customer.customer.model_dump_json()
        }
    )


async def post_order(
    http_client: HttpxClient,
    order: OrderIn
):
    await http_client.request(
        "POST",
        f"{configs.RETAIL_CRM_HOST}/api/v5/orders/create",
        data={
            "order": json.dumps(
                {
                    "number": order.number,
                    "customer": order.customer.model_dump(mode="json"),
                    "items": [item.model_dump(mode="json") for item in order.items]
                }
            )
        }
    )


async def fetch_orders_page_by_customer_id(
    http_client: HttpxClient,
    pagination_limit: int,
    pagination_offset: int,
    customer_id: int,
) -> Paginated[OrderOut]:
    params = build_params(
        {
            "filter[customerId]": customer_id,
        },
        limit=pagination_limit,
        page=int(pagination_offset/pagination_limit) + 1
    )

    json_response = await http_client.request(
        "GET",
        f"{configs.RETAIL_CRM_HOST}/api/v5/orders",
        params=params,
    )
    return Paginated(
        limit=json_response['pagination']['limit'],
        offset=json_response['pagination']['limit'] * (json_response['pagination']['currentPage'] - 1),
        total=json_response['pagination']['totalCount'],
        data=[OrderOut(**order) for order in json_response['orders']]
    )


async def post_payment(
    http_client: HttpxClient,
    order_id: int,
    payment: PaymentIn,
):
    payment_data = payment.model_dump(mode='json')
    payment_data["order"] = {"id": order_id}

    await http_client.request(
        "POST",
        f"{configs.RETAIL_CRM_HOST}/api/v5/orders/payments/create",
        data={
            "payment": json.dumps(payment_data)
        }
    )

    # import retailcrm


    # client = retailcrm.v5(configs.RETAIL_CRM_HOST, configs.RETAIL_CRM_API_KEY)
    # client.order_payment_create(
    #     {"order": {"id": order_id}, "amount": payment.amount}
    # )
