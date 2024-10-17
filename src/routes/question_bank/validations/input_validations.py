from enum import Enum


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple-choice"
    CHECKBOX = "Checkbox"
    FREE_RESPONSE = "Free-response"
    GRAPH = "Graph"
    DROP_DOWN_MENU = "Drop-down-Menu"
    DRAG_AND_DROP = "Drag-and-Drop"

class AssignmentType(str, Enum):
    STAAR = "STAAR"
    SAT = "SAT"
    ACT = "ACT"
    TSI = "TSI"

class Category(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"

class DifficultyType(str, Enum):
    EASY = "Easy"
    AVERAGE = "Average"
    ADVANCE = "Advance"