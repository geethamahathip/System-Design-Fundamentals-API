from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.routers.links import router as links_router
from app.routers.redirect import router as redirect_router
from app.routes.health import router as health_router
from app.routes.readiness import router as readiness_router
from app.core.middleware import RequestMiddleware
from app.core.errors import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

from threading import Thread
from app.workers.click_worker import start_click_worker

import logging
logger=logging.getLogger("app")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("APPLICATION_STARTUP")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("APPLICATION_SHUTDOWN")

# routers
app.include_router(health_router)
app.include_router(links_router)
app.include_router(redirect_router)
app.include_router(readiness_router)

# logging
logging.basicConfig(level=logging.INFO)

# middleware
app.add_middleware(RequestMiddleware)

# exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

#worker_thread = Thread(target=start_click_worker, daemon=True)
#worker_thread.start()

@app.on_event("shutdown")
def shutdown_event():
    print("APPLICATION_SHUTDOWN")