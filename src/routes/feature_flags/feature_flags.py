from fastapi import Request, APIRouter, Body, status
from src.routes.feature_flags.service import FeatureFlags


router = APIRouter()

feature_flag = FeatureFlags()

@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def feature_list(query: Request) -> dict:
    query_dict = dict(query.query_params)
    return await feature_flag.feature_list(query_dict)

@router.post("/create", response_model=dict, status_code=status.HTTP_200_OK)
async def create_school_features(school_features: dict) -> dict:
    return await feature_flag.create_school_features(school_features)

@router.put("/update/{school_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_school_features(school_id: str, updated_data: dict) -> dict:
    return await feature_flag.update_school_features(school_id, updated_data)

# @router.post("/create", response_model=dict)
# async def create_question(question_data: dict) -> dict:
#     return await feature_flag.create_question(question_data)

# @router.get("/{question_id}", response_model=dict)
# async def fetch_question(question_id: str) -> dict:
#     return await feature_flag.fetch_question(question_id)

# @router.delete("/delete/{question_id}", response_model=dict)
# async def delete_question(question_id: str) -> dict:
#     return await feature_flag.delete_question(question_id)