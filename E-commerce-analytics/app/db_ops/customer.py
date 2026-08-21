from app.routers import customers
from fastapi import HTTPException
from datetime import datetime

from app.database import SessionLocal
from app import models
from app.models import Customer




def create_customer(name: str, email: str, phone: str):

    db = SessionLocal()

    try:
        customer = Customer(
            name = name, 
            email = email,
            phone = phone
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return {
            "message": "Customer created successfully",
            "customer_id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone
        }


    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))