from fastapi import APIRouter

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get("/")
def get_analytics_summary():
    return {"message": "Analytics endpoint active"}
