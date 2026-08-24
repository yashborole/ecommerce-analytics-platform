from fastapi import APIRouter, HTTPException
# Import the function from db_ops:
from app.db_ops import products as product_ops

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/")
async def create_product(name : str, description:str, category: str, price: float, stock: str):

    try:

        result = product_ops.create_product(name=name,description=description,category=category,price=price,stock=stock)

        if "error" in result:
            raise HTTPException(status_code=400,detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))