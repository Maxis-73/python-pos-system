from fastapi import FastAPI
from app.core.settings import settings
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from app.modules.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Routes
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the POS system API"}

@app.get("/health")
async def health():
    return {"status": "OK"}