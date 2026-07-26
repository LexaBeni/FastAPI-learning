from fastapi import FastAPI, Request
import joblib
from contextlib import asynccontextmanager
from routers.status import router as status_router
from routers.prediction import router as prediction_router
from routers.auth import router as auth_router
import time
from logger import logger
from core.settings import settings
from core.database import Base, engine
from core.exception import AppException
from fastapi.responses import JSONResponse
from core.database import SessionLocal
from services.bootstrap_service import ensure_default_admin



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model...")
    app.state.model = joblib.load(settings.model_path)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database is successfully connected.")
    except Exception as e:
        print(e)
        logger.critical("Database connection failed.")
        
        raise RuntimeError("Database connection failed")
    
    with SessionLocal() as db:
        ensure_default_admin(db)

    yield

    logger.warning("Server is shutting down...")

app =  FastAPI(lifespan=lifespan)

@app.middleware("http")
async def middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    response.headers["X-Process-Time"] = str(duration)

    logger.info(f"Completed in {duration:.4f} seconds")

    return response

app.include_router(status_router)
app.include_router(prediction_router)
app.include_router(auth_router)

@app.exception_handler(AppException)
def prediction_not_found(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )