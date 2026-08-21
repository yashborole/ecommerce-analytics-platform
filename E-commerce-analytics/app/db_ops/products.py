from fastapi import HTTPException
from app.database import SessionLocal
from app.models.product import Product


def create_product(name: str, description: str, category: str, price: float, stock:str):

    db = SessionLocal()
    try:
        product = Product(
            name = name,
            description = description,
            category = category,
            price = price,
            stock = stock

        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "message": "Product created successfully",
            "product_id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock
        }

    except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))