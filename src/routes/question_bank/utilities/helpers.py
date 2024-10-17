from src.routes.question_bank.models import (
    MultipleChoiceQuestion, CheckboxQuestion, FreeResponseQuestion, 
    GraphQuestion, DropdownMenuQuestion, DragAndDropQuestion, 
)


def question_serializer(question: dict) -> dict:
    return {
        "_id": str(question["_id"]),
        "question": question["question"],
        "choices": question["choices"],
        "correctAnswer": question["correctAnswer"],
        "questionDetails": question["questionDetails"],
        "assignmentType": question["assignmentType"],
        "questionType": question["questionType"],
        "difficulty": question["difficulty"],
        "teksCode": question["teksCode"],
        "points": question["points"],
        "category": question["category"],
        "deleted": question["deleted"],
        "createdDate": question["createdDate"],
        "updatedDate": question["updatedDate"],
        "deletedDate": question["deletedDate"],
    }

question_type_map = {
    "Multiple-choice": MultipleChoiceQuestion,
    "Checkbox": CheckboxQuestion,
    "Free-response": FreeResponseQuestion,
    "Graph": GraphQuestion,
    "Drop-down-Menu": DropdownMenuQuestion,
    "Drag-and-Drop": DragAndDropQuestion,
}