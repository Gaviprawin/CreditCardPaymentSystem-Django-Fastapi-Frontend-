from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from payment_api.routers.payment import router as payment_router


app = FastAPI(
    title="Credit Card Payment System",
    description="FastAPI Payment Processing Service",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    payment_router
)


@app.get("/")
def home():

    return {
        "message":
            "Payment Processing API is running",

        "status":
            "success"
    }