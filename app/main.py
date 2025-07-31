from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import api, models, logging_conf
from .db import engine
from .config import get_settings

settings = get_settings()

app = FastAPI(
    title="Math Microservice",
    version="2.0.0",
    description="pow / fib / factorial + logging, auth & metrics",
    docs_url="/docs",
)

if settings.prometheus_enabled:
    Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logging_conf.logger.info("service_started")

app.include_router(api.router)
