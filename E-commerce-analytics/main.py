from fastapi import FastAPI
from app.routers import order, customers, products, analytics

app = FastAPI(
    title="E-commerce Analytics API",
    version="1.0.0"
)

app.include_router(order.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(analytics.router)