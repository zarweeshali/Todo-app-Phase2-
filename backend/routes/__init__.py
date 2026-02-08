"""
Routes package initialization
"""

from fastapi import APIRouter
from backend.routes.todos import router as todos_router
from backend.routes.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(todos_router)
api_router.include_router(auth_router)

__all__ = ["api_router"]
