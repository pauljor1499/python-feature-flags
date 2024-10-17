from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import DATABASE
from src.routes.feature_flags.models import FeatureFlag

def feature_serializer(feature: dict) -> dict:
    return {
        "_id": str(feature["_id"]),
        "name": feature["name"],
        "enabled": feature["enabled"],
        "school": str(feature["school"]),
    }

class FeatureFlags:
    def __init__(self):
        if DATABASE is not None:
            self.collection = DATABASE["feature_flags"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
    

    async def feature_list(self, query: dict) -> dict:
        try:
            filter_criteria = {}

            if "school_id" in query and query["school_id"]:
                filter_criteria["school"] = ObjectId(query["school_id"])

            if "feature_name" in query and query["feature_name"]:
                filter_criteria["name"] = query["feature_name"]

            if "enabled" in query:
                if isinstance(query["enabled"], str):
                    filter_criteria["enabled"] = query["enabled"].lower() == "true"
                else:
                    filter_criteria["enabled"] = query["enabled"]

            features = await self.collection.find(filter_criteria).to_list(100)

            return {"features": [feature_serializer(feature) for feature in features]}

        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while fetching features")
        
    
    async def create_school_features(self, school: dict) -> dict:
        all_features = ["Dashboard", "Settings", "Classes"]
        inserted_features = []

        try:
            school_id = ObjectId(school["school"]["_id"])
            
            for feature_name in all_features:
                # Check if the feature is in the active_features list
                active_feature = next((feature for feature in school["school"]["active_features"] if feature["name"] == feature_name), None)
                is_enabled = active_feature["enabled"] if active_feature else False

                feature_data = {
                    "name": feature_name,
                    "enabled": is_enabled,
                    "school": school_id
                }

                # Check if the feature already exists for this school
                existing_feature = await self.collection.find_one(
                    {"name": feature_name, "school": school_id}
                )

                if not existing_feature:
                    # Insert the new feature into the collection
                    insert_result = await self.collection.insert_one(feature_data)
                    feature_data["_id"] = insert_result.inserted_id  # Keep ObjectId for storage
                    inserted_features.append(feature_serializer(feature_data))
                else:
                    # Update the existing feature if the enabled status has changed
                    if existing_feature['enabled'] != is_enabled:
                        await self.collection.update_one(
                            {"_id": existing_feature["_id"]},
                            {"$set": {"enabled": is_enabled}}
                        )
                    inserted_features.append(feature_serializer(existing_feature))

            return {
                "school": {
                    "_id": str(school_id),
                    "all_features": inserted_features
                }
            }

        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while creating school features")


    async def update_school_features(self, school_id: str, features: dict) -> dict:
        updated_features = []
        missing_features = []

        try:
            school_id = ObjectId(school_id)
            
            # Loop through the features from the payload
            for feature in features["school"]["features"]:
                feature_name = feature["name"]
                is_enabled = feature["enabled"]

                # Check if the feature already exists for this school
                existing_feature = await self.collection.find_one(
                    {"name": feature_name, "school": school_id}
                )

                if existing_feature:
                    # Update the existing feature if the enabled status has changed
                    if existing_feature['enabled'] != is_enabled:
                        await self.collection.update_one(
                            {"_id": existing_feature["_id"]},
                            {"$set": {"enabled": is_enabled}}
                        )
                    updated_features.append(feature_serializer(existing_feature))
                else:
                    missing_features.append(feature_name)

            # If there are missing features, raise an error
            if missing_features:
                raise HTTPException(
                    status_code=404,
                    detail=f"Features not found: {', '.join(missing_features)}"
                )

            return {
                "school": {
                    "_id": str(school_id),
                    "all_features": updated_features
                }
            }

        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while updating school features")