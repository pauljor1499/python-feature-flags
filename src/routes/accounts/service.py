from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type

class AccountsService:
    def __init__(self, db_client):
        self.database = db_client
        self.collection = self._get_users_collection()

    def _get_users_collection(self):
        """
        Retrieves the 'users' collection from the connected database.
        Raises an exception if the database is unavailable.
        """
        if self.database is None:
            raise HTTPException(status_code=500, detail="Unable to connect to the database.")
        return self.database["users"]

