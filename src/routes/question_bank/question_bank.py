from fastapi import Request, APIRouter, Body, status
from src.routes.question_bank.service import QuestionBankService
from src.routes.question_bank.models import QuestionUpdate
from src.routes.question_bank.utilities.payloads import questions


router = APIRouter()

question_bank = QuestionBankService()

@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def fetch_questions(query: Request) -> dict:
    query_dict = dict(query.query_params)
    return await question_bank.fetch_questions(query_dict)

@router.post("/create", response_model=dict, status_code=status.HTTP_200_OK)
async def create_question(question_data: dict = Body(openapi_examples=questions)) -> dict:
    return await question_bank.create_question(question_data)

@router.get("/{question_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def fetch_question(question_id: str) -> dict:
    return await question_bank.fetch_question(question_id)

@router.put("/update/{question_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_question(question_id: str, updated_data: QuestionUpdate) -> dict:
    return await question_bank.update_question(question_id, updated_data)

@router.delete("/delete/{question_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_question(question_id: str) -> dict:
    return await question_bank.delete_question(question_id)