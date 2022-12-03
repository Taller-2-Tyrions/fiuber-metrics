from fastapi import FastAPI
from .routers import metrics
from fastapi.middleware.cors import CORSMiddleware
from .services import rabbit_services
from threading import Thread

app = FastAPI()

new_thread = Thread(target=rabbit_services.run_rabbit_service)

new_thread.start()
# rabbit_services.run_rabbit_service()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics.router)


@app.get("/")
async def root():
    return {"msg": "Fiuber-metrics"}
