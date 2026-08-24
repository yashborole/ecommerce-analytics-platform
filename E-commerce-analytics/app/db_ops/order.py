from sqlalchemy import text
from alembic.util import status
from fastapi import HTTPException
from datetime import datetime

from app.database import SessionLocal
from app import models


def create_order(customer_id: int, product_id: int, quantity: int):

    db = SessionLocal()

    try:

        customer = db.query(models.Customer).filter(
            models.Customer.id == customer_id
        ).first()

        if not customer:
            return {
                "error": "Customer not found"
            }

        product = db.query(models.Product).filter(
            models.Product.id == product_id
        ).first()

        if not product:
            return {
                "error": "Product not found"
            }

        if quantity <= 0:
            return {
                "error": "Quantity must be greater than 0"
            }

        if product.stock < quantity:
            return {
                "error": "Insufficient stock"
            }

        total_price = product.price * quantity

        order = models.Order(
            order_id=f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_id=customer_id,
            order_date=datetime.now(),
            order_status="Pending",
            order_total=total_price
        )

        db.add(order)
        db.flush()

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price,
            subtotal=total_price
        )

        db.add(order_item)

        product.stock = int(product.stock) - quantity

        db.commit()
        db.refresh(order)

        return {
            "message": "Order created successfully",
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": product.price,
            "order_total": order.order_total,
            "order_date": order.order_date,
            "order_status": order.order_status
        }

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))



def get_orders():
    db = SessionLocal()
    try:
        orders = db.query(models.Order).all()
        
        return orders

    except Exception as e:
        return {"error": str(e)}


def get_order(order_id: int):

    db = SessionLocal()

    try:
        order_data = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order_data:
            return {"error": "Order not found"}
        return order_data

    except Exception as e:

        return {"error": str(e)}
    finally:
        db.close()


def cancel_order(order_id: int):

    db = SessionLocal()

    query = """
        UPDATE orders
        SET order_status = 'Cancelled'
        WHERE id = :order_id
        RETURNING id, order_id, order_status
    """

    try:

        if not order_id:
            return {
                "error": "Order id not found"
            }

        result = db.execute(
            text(query),
            {
                "order_id": order_id
            }
        )

        order = result.fetchone()

        if not order:
            return {
                "error": "Order not found"
            }

        db.commit()

        return {
            "message": "Order cancelled successfully",
            "order_id": order.order_id,
            "order_status": order.order_status
        }

    except Exception as e:

        return {
            "error": str(e)
        }



def update_order_status(order_id:int, order_status : str):
    db = SessionLocal()

    query = """update orders 
            set order_status = :order_status
            where id = :order_id
            RETURNING id, order_id, order_status
            """

    try:
        if not order_id:
            return {"error":"order id not found"}
        
        result = db.execute(text(query),{
        "order_id": order_id,
        "order_status": order_status})        
        db.commit()

        return {
            "message":"order status update suceesfully",
            "order_id":order_id,
            "order_status":order_status
        }        

    except Exception as e:
        return {"error": str(e)}
