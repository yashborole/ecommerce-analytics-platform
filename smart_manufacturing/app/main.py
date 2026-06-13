from fastapi import FastAPI
from app.routes.login import router as users_router

app = FastAPI(title="My API")

app.include_router(users_router)