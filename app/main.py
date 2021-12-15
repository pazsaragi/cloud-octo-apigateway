import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.settings import ALLOWED_HOSTS
from app.routers import auth, users
from app.logger import get_logger


app = FastAPI()
logger = get_logger(__name__)
origins = ALLOWED_HOSTS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_req_res(request: Request, call_next):
    start_time = time.time()
    logger.info(
        f"Path: {request.url}, Method: {request.method}, Headers: {request.headers}"
    )
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Status: {response.status_code}, Time: {process_time}")
    return response


@app.get("/health")
async def ping():
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(auth.router)
