from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Union
from datetime import datetime, timezone
# from beanie import Document
from src.routes.question_bank.validations.input_validations import QuestionType, AssignmentType, Category, DifficultyType
from src.routes.question_bank.validations.field_validations import (
    validate_question_field,
    validate_choices_field,
    validate_correct_answer_field,
    validate_question_details_field,
    validate_assignment_type_field,
    validate_question_type_field,
    validate_difficulty_field,
    validate_teks_code_field,
    validate_points_field,
    validate_category_field,
    validate_deleted_field,
    validate_deleted_date_field,
    validate_created_date_field,
    validate_updated_date_field
)


class Item(BaseModel):
    id: int  # Custom ID
    text: str = Field(..., min_length=1, max_length=300)

class Select(BaseModel):
    id: int  # Custom ID
    items: List[Item]

class Answer(BaseModel):
    id: int  # Custom ID
    answer: str = Field(..., min_length=1, max_length=300)

class CorrectAnswer(BaseModel):
    answers: Union[List[Answer], List[str], str]  # Can be a list of Answer objects, a list of strings, or a single string
    answerDetails: str = Field(None, min_length=1, max_length=300)

class QuestionBase(BaseModel):
    # Required fields
    question: str = Field(..., min_length=1, max_length=300)
    correctAnswer: CorrectAnswer
    assignmentType: AssignmentType
    difficulty: DifficultyType
    points: str = Field(..., min_length=1, max_length=3)
    questionType: QuestionType
    createdDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted: bool = False
    # Optional fields
    updatedDate: Optional[datetime] = None
    deletedDate: Optional[datetime] = None
    questionDetails: Optional[str] = Field(None, min_length=1, max_length=300)
    teksCode: Optional[str] = Field(None, min_length=1, max_length=3)
    category: Optional[Category] = None
    
    @model_validator(mode='before')
    def validate_fields(cls, values):
        validate_question_field(values)
        validate_choices_field(values)
        validate_correct_answer_field(values)
        validate_question_details_field(values)
        validate_assignment_type_field(values)
        validate_question_type_field(values)
        validate_difficulty_field(values)
        validate_teks_code_field(values)
        validate_points_field(values)
        validate_category_field(values)
        validate_deleted_field(values)
        validate_deleted_date_field(values)
        validate_created_date_field(values)
        validate_updated_date_field(values)
        return values

class MultipleChoiceQuestion(QuestionBase):
    choices: List[Item]
    questionType: QuestionType = QuestionType.MULTIPLE_CHOICE

class CheckboxQuestion(QuestionBase):
    choices: List[Item]
    questionType: QuestionType = QuestionType.CHECKBOX

class FreeResponseQuestion(QuestionBase):
    questionType: QuestionType = QuestionType.FREE_RESPONSE
    choices: Optional[str] = None

class GraphQuestion(QuestionBase):
    questionType: QuestionType = QuestionType.GRAPH
    choices: Optional[str] = None

class DropdownMenuQuestion(QuestionBase):
    choices: List[Select]
    questionType: QuestionType = QuestionType.DROP_DOWN_MENU

class DragAndDropQuestion(QuestionBase):
    choices: List[Item]
    questionType: QuestionType = QuestionType.DRAG_AND_DROP

class QuestionUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1, max_length=300)
    choices: Optional[List[Union[Item, Select]]] = None
    correctAnswer: Optional[CorrectAnswer] = None
    questionDetails: Optional[str] = Field(None, min_length=1, max_length=300)
    assignmentType: Optional[AssignmentType] = None
    difficulty: Optional[DifficultyType] = None
    teksCode: Optional[str] = Field(None, min_length=1, max_length=3)
    points: Optional[str] = Field(None, min_length=1, max_length=3)
    category: Optional[Category] = None
    questionType: Optional[QuestionType] = None
    updatedDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
