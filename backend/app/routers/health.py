"""Health-check route so the frontend (and operators) can see if the API is up."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "API is running",
    }
