from fastapi import FastAPI

from app.routers import order, customers, products

app = FastAPI()

app.include_router(order.router)
app.include_router(customers.router)
app.include_router(products.router)