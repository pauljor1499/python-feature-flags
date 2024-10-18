from pydantic import BaseModel
from typing import Optional, List


class FeatureFlag(BaseModel):
    name: str
    enabled: bool
    deleted: Optional[bool] = None
    school: str


class CreateFeatureFlag(BaseModel):
    school_id: str
    features: List[FeatureFlag]