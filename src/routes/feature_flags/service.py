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
            features = await self.collection.find().to_list(100)
            return {"features": [feature_serializer(feature) for feature in features]}
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while fetching all features")
        
    
    async def create_school_features(self, school: dict) -> dict:
        all_features = ["Dashboard", "Settings", "Classes"]
        inserted_features = []

        try:
            # Retrieve the school ID from the payload and convert it to ObjectId
            school_id = ObjectId(school["school"]["_id"])
            
            # Loop through all features defined in all_features
            for feature_name in all_features:
                # Check if the feature is in the active_features list
                active_feature = next((feature for feature in school["school"]["active_features"] if feature["name"] == feature_name), None)
                is_enabled = active_feature["enabled"] if active_feature else False  # Default to False if not found

                feature_data = {
                    "name": feature_name,
                    "enabled": is_enabled,
                    "school": str(school_id)  # Store the school ID as a string for MongoDB
                }

                # Check if the feature already exists for this school
                existing_feature = await self.collection.find_one(
                    {"name": feature_name, "school": school_id}
                )

                if not existing_feature:
                    # Insert the new feature into the collection
                    insert_result = await self.collection.insert_one(feature_data)
                    feature_data["_id"] = str(insert_result.inserted_id)  # Convert ObjectId to string
                    inserted_features.append(feature_data)  # Add the created feature to the list
                else:
                    # Update the existing feature if the enabled status has changed
                    if existing_feature['enabled'] != is_enabled:
                        await self.collection.update_one(
                            {"_id": existing_feature["_id"]},
                            {"$set": {"enabled": is_enabled}}
                        )
                    existing_feature["_id"] = str(existing_feature["_id"])  # Convert ObjectId to string
                    inserted_features.append(existing_feature)  # Include the existing feature

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