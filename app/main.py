
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database import Base, engine
from app import models
from app.routes.jobs import router as jobs_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title="Bulk Certificate Generator",
    description="Generate and download personalized PDF certificates in bulk.",
    version="1.0.0",
)


# Register existing API routes
app.include_router(jobs_router)


# Serve the frontend dashboard
@app.get("/", include_in_schema=False)
def home():
    html_file = Path(__file__).parent / "static" / "index.html"
    return FileResponse(html_file, media_type="text/html")


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}
