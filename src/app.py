from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.question_bank.question_bank import router as QuestionBank
from src.connection import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await init_db()
    yield
    # Shutdown event (if needed)
    # Perform any cleanup actions here

app = FastAPI(
    title="Question Bank API",
    description="Owned by: MathMattersTx Team",
    version="Version 1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Server is up and running."}

app.include_router(QuestionBank, tags=["Questions"], prefix="/questions")