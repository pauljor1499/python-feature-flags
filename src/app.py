from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.connection import init_db
from contextlib import asynccontextmanager
from src.routes.question_bank.question_bank import router as QuestionBank
from src.routes.feature_flags.feature_flags import router as FeatureFlags


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Question Bank API",
    description="Owned by: EruditionTx Team",
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
app.include_router(FeatureFlags, tags=["Feature Flags"], prefix="/feature-flags")