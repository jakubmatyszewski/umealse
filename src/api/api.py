"""Aggregate endpoint routes for main."""
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from src.api.v1.users import user_router

api_router = APIRouter()

api_router.include_router(user_router)


@api_router.get("/docs", include_in_schema=False)
async def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
