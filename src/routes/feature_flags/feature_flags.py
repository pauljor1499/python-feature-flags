from fastapi import Request, APIRouter, status
from src.routes.feature_flags.service import FeatureFlags


router = APIRouter()

feature_flag = FeatureFlags()

@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def fetch_all_school_features(query: Request) -> dict:
    query_dict = dict(query.query_params)
    return await feature_flag.fetch_all_school_features(query_dict)

@router.get("/{school_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def fetch_school_features(school_id: str, query: Request) -> dict:
    query_dict = dict(query.query_params)
    return await feature_flag.fetch_school_features(school_id, query_dict)

@router.post("/create", response_model=dict, status_code=status.HTTP_200_OK)
async def create_school_features(school_features: dict) -> dict:
    return await feature_flag.create_school_features(school_features)

@router.put("/update/{school_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_school_features(school_id: str, updated_data: dict) -> dict:
    return await feature_flag.update_school_features(school_id, updated_data)

@router.delete("/delete/{school_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_question(school_id: str) -> dict:
    return await feature_flag.delete_school_features(school_id)