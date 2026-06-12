from fastapi import FastAPI
from app.routes import router as users_router

app = FastAPI(title="My API")

app.include_router(users_router)