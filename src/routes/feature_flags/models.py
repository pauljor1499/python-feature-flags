from pydantic import BaseModel


class FeatureFlag(BaseModel):
    name: str
    enabled: bool