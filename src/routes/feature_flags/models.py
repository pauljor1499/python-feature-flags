from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId


class FeatureFlag(BaseModel):
    # required fields from the request payload
    name: str
    enabled: bool
    # optional fields
    school: Optional[ObjectId] = None
    createdDate: Optional[datetime] = None
    deleted: Optional[bool] = None
    updatedDate: Optional[datetime] = None
    deletedDate: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True

class CreateFeatureFlag(BaseModel):
    school_id: str
    features: List[FeatureFlag]