from fastapi import Request, APIRouter, Body
from src.routes.feature_flags.service import FeatureFlags


router = APIRouter()

account_service = FeatureFlags()

# @router.post("/create", response_model=dict)
# async def create_question(question_data: dict) -> dict:
#     return await account_service.create_question(question_data)

# @router.get("/{question_id}", response_model=dict)
# async def fetch_question(question_id: str) -> dict:
#     return await account_service.fetch_question(question_id)

# @router.delete("/delete/{question_id}", response_model=dict)
# async def delete_question(question_id: str) -> dict:
#     return await account_service.delete_question(question_id)