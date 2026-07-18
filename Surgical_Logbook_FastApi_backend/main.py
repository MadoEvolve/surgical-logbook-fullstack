from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routers import procedures, hospitals, users, auth, logs, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(root_path="/logbook/v1", lifespan=lifespan)
# CORS handle
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(procedures.router)
app.include_router(hospitals.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(stats.router)
  
@app.get("/")
async def root():
    return {"message": "Hello Mado!"}


