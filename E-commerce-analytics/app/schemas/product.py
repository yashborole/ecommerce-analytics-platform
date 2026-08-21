from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category: str
    price: float
    stock: int