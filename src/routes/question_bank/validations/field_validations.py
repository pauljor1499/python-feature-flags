

def validate_question_field(values):
    if 'question' not in values:
        raise ValueError('question field is missing.')
    return values

def validate_choices_field(values):
    if values["questionType"] in ["Free-response", "Graph"]:
        if values["choices"] is not None:
            raise ValueError('choices field must be null.')
    else:
        if 'choices' not in values:
            raise ValueError('choices field is missing.')
    return values

def validate_correct_answer_field(values):
    if 'correctAnswer' not in values:
        raise ValueError('correctAnswer field is missing.')
    return values

def validate_question_details_field(values):
    if 'questionDetails' not in values:
        raise ValueError('questionDetails field is missing.')
    return values

def validate_assignment_type_field(values):
    if 'assignmentType' not in values:
        raise ValueError('assignmentType field is missing.')
    return values

def validate_question_type_field(values):
    if 'questionType' not in values:
        raise ValueError('questionType field is missing.')
    return values

def validate_difficulty_field(values):
    if 'difficulty' not in values:
        raise ValueError('difficulty type field is missing.')
    return values

def validate_teks_code_field(values):
    if values["assignmentType"] != "STAAR" and values["teksCode"] is not None:
        raise ValueError('teksCode must be null.')
    elif 'teksCode' not in values:
        raise ValueError('teksCode is missing.')
    return values

def validate_points_field(values):
    if 'points' not in values:
        raise ValueError('points field is missing.')
    return values

def validate_category_field(values):
    if values["assignmentType"] != "STAAR" and values["category"] is not None:
        raise ValueError('category field must be null.')
    elif 'category' not in values:
        raise ValueError('category field is missing.')
    return values

def validate_deleted_field(values):
    if 'deleted' in values:
        raise ValueError("deleted field must not be included in the payload.")
    return values

def validate_deleted_date_field(values):
    if 'deletedDate' in values:
        raise ValueError("deletedDate field must not be included in the payload.")
    return values

def validate_created_date_field(values):
    if 'createdDate' in values:
        raise ValueError("createdDate field must not be included in the payload.")
    return values

def validate_updated_date_field(values):
    if 'updatedDate' in values:
        raise ValueError("updatedDate field must not be included in the payload.")
    return values