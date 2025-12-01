"""
AI Meeting Assistant - Main Application Entry

This is the main entry point for the FastAPI application.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application instance
app = FastAPI(
    title="AI Meeting Assistant",
    description="An AI-powered meeting management system that helps automatically generate meeting minutes, extract action items, and integrate with external task systems.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the service status and version information.
    Use this endpoint to verify the service is running correctly.
    """
    return {
        "status": "healthy",
        "service": "ai-meeting-assistant",
        "version": "0.1.0",
    }


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint.
    
    Returns a welcome message and links to documentation.
    """
    return {
        "message": "Welcome to AI Meeting Assistant API",
        "docs": "/docs",
        "health": "/health",
    }

