
from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes.jobs import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator",
    description="Generate and track certificates in bulk",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
