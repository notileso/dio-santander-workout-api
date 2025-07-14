from fastapi import FastAPI
from .routers import router

app = FastAPI(
    title="Workout API",
)

app.include_router(router, prefix="/api/v1")
