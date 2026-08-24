from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import schemas
from app.database import get_db
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)
from app.db_ops import order
from app.database import SessionLocal

db=SessionLocal()

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)

@router.post("/")
async def create_order(customer_id: int, product_id: int, quantity: int):
    try:

        result = order.create_order(customer_id=customer_id, product_id=product_id,quantity=quantity)

        if "error" in result:
            raise HTTPException(status_code=400,detail=result["error"])

        return result

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.post("/")
async def get_orders():
    try:

        result = order.get_orders()

        if "error" in result:
            raise HTTPException(status_code=400)

        return result

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.get("/{order_id}")
def get_order(order_id: int):

    try:

        result = order.get_order(order_id=order_id)

        if not result:
            raise HTTPException(status_code=404,detail=result)
        return result

    except Exception as e:

        raise HTTPException(status_code=404,detail=str(e))

@router.get("/{order_id}/cancel")
def cancel_order(order_id: int):

    try:

        result = order.cancel_order(order_id=order_id)

        if "error" in result:
            raise HTTPException(status_code=404,detail=result["error"])
        return result

    except Exception as e:

        raise HTTPException(status_code=404,detail=str(e))


@router.put("/update_order_status")
def update_order_status(order_id: int, order_data: OrderStatusUpdate):

    try:

        result = order.update_order_status(order_id=order_id,order_status=order_data.order_status)

        if "error" in result:
            raise HTTPException(status_code=404,detail=result["error"])
        return result

    except Exception as e:

        raise HTTPException(status_code=404,detail=str(e))
