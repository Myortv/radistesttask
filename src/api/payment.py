from fastapi import APIRouter, Depends, Query

from src.schemas.payment import PaymentIn

from src.lib import retailcrm

from src.lib.send_request import HttpxClient, client_dependency


api = APIRouter()


@api.post("/")
async def create_payment(
    payment: PaymentIn,
    order_id: int = Query(..., description="Id of order bind payment to"),
    http_client: HttpxClient = Depends(client_dependency),
):
    """
    create and bind payment to the order
    """
    await retailcrm.post_payment(
        http_client,
        order_id,
        payment,
    )
    return {"details": "created"}
