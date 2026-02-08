"""
FastAPI application setup for Phase II Todo App
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_db, close_db
from backend.routes import api_router


# Startup event
def startup_event():
    """
    Initialize database on startup
    """
    init_db()
    print("Database initialized successfully")


# Shutdown event
def shutdown_event():
    """
    Close database connection on shutdown
    """
    close_db()
    print("Database connection closed")


# Create FastAPI app
app = FastAPI(
    title="Todo App Phase II API",
    description="Secure REST API for todo management with JWT authentication",
    version="1.0.0",
)

# Add event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# CORS middleware - Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local development
        "http://localhost:5173",      # Vite dev server
        os.getenv("FRONTEND_URL", ""),  # Production frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "todo-api"}


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Todo App Phase II API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
