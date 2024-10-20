from fastapi import HTTPException
from bson import ObjectId
from src.connection import DATABASE
from datetime import datetime, timezone
from src.routes.feature_flags.models import CreateFeatureFlag, FeatureFlag
from typing import Optional


def feature_serializer(feature: dict) -> dict:
    return {
        "_id": str(feature["_id"]),
        "name": feature["name"],
        "enabled": feature["enabled"],
        "school": str(feature["school"]),
        "deleted": feature["deleted"],
        "deletedDate": feature["deletedDate"],
        "createdDate": feature["createdDate"],
        "updatedDate": feature["updatedDate"],
    }

class FeatureFlags:
    def __init__(self):
        if DATABASE is not None:
            self.collection = DATABASE["feature_flags"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
    

    async def fetch_all_school_features(self, query: dict) -> dict:
        try:
            filter_criteria = {"deleted": False}

            if "school_id" in query and query["school_id"] is not None:
                filter_criteria["school"] = ObjectId(query["school_id"])

            if "feature_name" in query and query["feature_name"] is not None:
                filter_criteria["name"] = query["feature_name"]

            if "enabled" in query and query["enabled"] is not None:
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
    

    async def fetch_school_features(self, school_id: str, query: dict) -> dict:
        try:
            filter_criteria = {"school": ObjectId(school_id), "deleted": False}

            if "enabled" in query and query["enabled"] is not None:
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
        
    
    async def create_school_features(self, payload: dict) -> dict:
        all_features = ["Dashboard", "Settings", "Classes"]
        inserted_features = []

        try:
            # Validate and convert payload to CreateFeatureFlag model
            validated_payload = CreateFeatureFlag(**payload)
            school_id = ObjectId(validated_payload.school_id)

            # Iterate over the all_features to check for existence and insert/update
            for feature_name in all_features:
                is_enabled = next(
                    (feature.enabled for feature in validated_payload.features if feature.name == feature_name),
                    False
                )

                # Check if the feature already exists for this school
                existing_feature = await self.collection.find_one(
                    {"name": feature_name, "school": school_id}
                )

                if not existing_feature:
                    data = {
                        "name": feature_name,
                        "enabled": is_enabled,
                        "school": school_id,
                        "deleted": False,
                        "createdDate": datetime.now(timezone.utc),
                    }
                    feature_data = FeatureFlag(**data)
                    feature_data_dict = feature_data.dict()
                    insert_result = await self.collection.insert_one(feature_data_dict)  # Use .dict() for insertion
                    feature_data_dict["_id"] = insert_result.inserted_id  # Keep ObjectId for storage
                    inserted_features.append(feature_serializer(feature_data_dict))
                else:
                    # Update the existing feature if the enabled status has changed
                    if existing_feature['enabled'] != is_enabled:
                        update_data = {
                            "enabled": is_enabled,
                            "updatedDate": datetime.now(timezone.utc),
                        }
                        await self.collection.update_one(
                            {"_id": existing_feature["_id"]},
                            {"$set": update_data}
                        )
                        # After updating, we fetch the updated feature to append to the list
                        updated_feature = await self.collection.find_one(
                            {"_id": existing_feature["_id"]}
                        )
                        inserted_features.append(feature_serializer(updated_feature))
                    else:
                        # If no update was needed, append the existing feature
                        inserted_features.append(feature_serializer(existing_feature))

            return {
                "data": {
                    "features_added": inserted_features
                }
            }

        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail=f"Error while creating school features: {str(e)}")


    async def update_school_features(self, school_id: str, features: dict) -> dict:
        updated_features = []
        missing_features = []

        try:
            school_id = ObjectId(school_id)
            feature_list = features["features"]

            # Loop through the features from the payload
            for feature in feature_list:
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
                            {"$set": {"enabled": is_enabled, "updatedDate": datetime.now(timezone.utc)}}
                        )
                        # Fetch the updated feature to append to the list
                        updated_feature = await self.collection.find_one(
                            {"_id": existing_feature["_id"]}
                        )
                        updated_features.append(feature_serializer(updated_feature))
                    else:
                        # If no change was made, append the existing feature
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
                "data": {
                    "school_id": str(school_id),
                    "updated_features": updated_features
                }
            }

        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while updating school features")
    

    async def delete_school_features(self, school_id: str) -> dict:
        if not ObjectId.is_valid(school_id):
            raise HTTPException(status_code=400, detail="Invalid school ID format")
        
        # Fetch the features associated with the school_id
        school_features = await self.fetch_school_features(school_id, {})
        
        if school_features is None:
            raise HTTPException(status_code=404, detail="School features not found")
        
        try:
            # Update all documents matching the school_id
            result = await self.collection.update_many(
                {"school": ObjectId(school_id)},
                {"$set": {"deleted": True, "deletedDate": datetime.now(timezone.utc)}}
            )
            
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="No matching features found for the school")
            
            updated_features = await self.fetch_school_features(school_id, {})
            
            return {"deleted": True, "data": updated_features}
        
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while deleting school features")