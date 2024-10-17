from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import DATABASE
from src.routes.feature_flags.models import FeatureFlag

class FeatureFlags:
    def __init__(self):
        if DATABASE is not None:
            self.collection = DATABASE["feature_flags"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
    
    async def feature_list(self, query: dict) -> dict:
        try:
            flags = await self.collection.find().to_list(100)
            return {"features": [FeatureFlag(**flag) for flag in flags]}
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while fetching all features")