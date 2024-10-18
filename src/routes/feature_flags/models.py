from pydantic import BaseModel
from typing import Optional, List


class FeatureFlag(BaseModel):
    name: str
    enabled: bool
    deleted: Optional[bool] = None
    school: Optional[str] = None


class CreateFeatureFlag(BaseModel):
    school_id: str
    features: List[FeatureFlag]