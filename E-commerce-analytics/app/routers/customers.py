from fastapi import APIRouter, HTTPException
from app.db_ops import customer as customer_ops

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],
)


@router.post("/")
async def create_customer(name: str, email: str, phone: str):
    try:
        result = customer_ops.create_customer(name=name, email=email, phone=phone)
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))