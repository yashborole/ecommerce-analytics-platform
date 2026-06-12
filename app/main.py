from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None
)


@app.get("/")
def home():
    return {"message": "Hello World", "project_name": settings.PROJECT_NAME}