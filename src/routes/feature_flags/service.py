from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import DATABASE

class FeatureFlags:
    def __init__(self):
        if DATABASE is not None:
            self.collection = DATABASE["questions"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")