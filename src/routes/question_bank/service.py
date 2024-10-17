from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import DATABASE
from src.routes.question_bank.models import QuestionUpdate, QuestionBase
from src.routes.question_bank.utilities.helpers import question_serializer, question_type_map
from datetime import datetime, timezone


class QuestionBankService:
    def __init__(self):
        if DATABASE is not None:
            self.collection = DATABASE["questions"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
            

    async def create_question(self, question_data: QuestionBase) -> dict:
        try:
            questionType = question_data["questionType"]
            if questionType not in question_type_map:
                raise HTTPException(status_code=400, detail="Invalid question type")
            QuestionModel: Type = question_type_map[questionType]
            question = QuestionModel(**question_data)
            question_dict = question.dict()
            result = await self.collection.insert_one(question_dict)
            new_question = await self.fetch_question(str(result.inserted_id))
            return {"new_question": new_question}
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while creating the question")


    async def fetch_question(self, question_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        try:
            question = await self.collection.find_one({"_id": ObjectId(question_id), "deleted": False})
            if not question:
                raise HTTPException(status_code=404, detail="Question not found")
            return question_serializer(question)
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while fetching the question")


    async def update_question(self, question_id: str, updated_question: QuestionUpdate) -> Optional[dict]:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        # Filter out None values from updated_question
        question_data = {k: v for k, v in updated_question.model_dump().items() if v is not None}
        question_data["teksCode"] = question_data.get("teksCode", None)
        question_data["category"] = question_data.get("category", None)
        existing_question = await self.fetch_question(question_id)
        if existing_question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": question_data}
            )
            updated_question = await self.fetch_question(question_id) if result.modified_count > 0 else None
            return {"updated_question": updated_question}
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while updating the question")


    async def delete_question(self, question_id: str) -> dict:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        question = await self.fetch_question(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": {"deleted": True, "deletedDate": datetime.now(timezone.utc)}}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Question not found")
            return {"deleted": True, "data": question}
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while deleting the question")


    async def fetch_questions(self, query: dict) -> dict:
        try:
            # Extract query parameters, supporting both snake_case and camelCase
            question_type = query.get("questionType") or query.get("question_type")
            assignment_type = query.get("assignmentType") or query.get("assignment_type")
            category = query.get("category")
            difficulty = query.get("difficulty")
            page = int(query.get("page", 1))  # Convert page to int with default of 1
            page_size = int(query.get("pageSize", query.get("page_size", 10)))  # Convert pageSize/page_size to int with default of 10

            # Pagination parameters
            skip = (page - 1) * page_size
            limit = page_size

            # Matching criteria for filtering
            match_criteria = {"deleted": False}
            if question_type:
                match_criteria["questionType"] = question_type
            if assignment_type:
                match_criteria["assignmentType"] = assignment_type
            if category:
                match_criteria["category"] = category
            if difficulty:
                match_criteria["difficulty"] = difficulty

            # Count total questions matching the criteria
            total_questions = await self.collection.count_documents(match_criteria)

            # Build aggregation pipeline for counting groupings
            aggregation_pipeline = [{"$match": match_criteria}] if match_criteria else []

            aggregation_pipeline.append({
                "$group": {
                    "_id": {
                        "assignmentType": "$assignmentType",
                        "questionType": "$questionType",
                        "category": "$category",
                        "difficulty": "$difficulty"
                    },
                    "count": {"$sum": 1}
                }
            })

            # Run the aggregation to get group counts
            counts = await self.collection.aggregate(aggregation_pipeline).to_list(100)

            # Initialize counts dictionaries
            assignment_types_counts = {"STAAR": 0, "TSI": 0, "SAT": 0, "ACT": 0}
            question_types_counts, categories_counts, difficulties_counts = {}, {}, {}

            for item in counts:
                # Extract group counts from the aggregation results
                assignment_type = item["_id"]["assignmentType"]
                question_type = item["_id"]["questionType"]
                category = item["_id"]["category"]
                difficulty = item["_id"]["difficulty"]
                count = item["count"]

                # Update counts
                if assignment_type in assignment_types_counts:
                    assignment_types_counts[assignment_type] += count
                if question_type:
                    question_types_counts[question_type] = question_types_counts.get(question_type, 0) + count
                if category:
                    categories_counts[category] = categories_counts.get(category, 0) + count
                if difficulty:
                    difficulties_counts[difficulty] = difficulties_counts.get(difficulty, 0) + count

            # Fetch questions with pagination
            questions_pipeline = [{"$match": match_criteria}] if match_criteria else []
            questions_pipeline.extend([{"$skip": skip}, {"$limit": limit}])

            questions = await self.collection.aggregate(questions_pipeline).to_list(limit)
            question_list = [question_serializer(question) for question in questions]

        except Exception as e:
            print(f"Error during data fetching: {e}")
            return {
                "data": {
                    "questions": [],
                    "assignmentTypes": {"STAAR": 0, "TSI": 0, "SAT": 0, "ACT": 0},
                    "questionTypes": {},
                    "categories": {},
                    "difficulties": {},
                },
                "pagination": {
                    "page": page,
                    "pageSize": page_size,
                    "totalCount": 0,
                    "totalQuestions": 0
                }
            }

        # Return the final response with questions and pagination
        return {
            "data": {
                "questions": question_list,
                "assignmentTypes": assignment_types_counts,
                "questionTypes": question_types_counts,
                "categories": categories_counts,
                "difficulties": difficulties_counts,
            },
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "totalCount": len(question_list),
                "totalQuestions": total_questions
            }
        }

