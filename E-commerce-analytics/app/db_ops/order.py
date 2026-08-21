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