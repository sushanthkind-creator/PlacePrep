from app.models import SCOPE_MIXED, SCOPE_SECTION
from app.utils.errors import ApiError

MIN_DURATION_MINUTES = 1
MAX_DURATION_MINUTES = 180
MAX_QUESTIONS = {SCOPE_SECTION: 50, SCOPE_MIXED: 60}


def question_count_limits(test, available):
    """Smallest and largest number of questions a student may choose for this test."""
    upper = min(available, MAX_QUESTIONS.get(test.scope, available))
    return min(3, upper), upper


def parse_start_attempt(data, test, available):
    errors = {}
    low, high = question_count_limits(test, available)

    count = data.get("question_count", min(test.default_question_count, high))
    if isinstance(count, bool) or not isinstance(count, int):
        errors["question_count"] = "Choose a whole number of questions."
    elif not low <= count <= high:
        errors["question_count"] = f"Choose between {low} and {high} questions."

    minutes = data.get("duration_minutes", test.default_duration_minutes)
    if isinstance(minutes, bool) or not isinstance(minutes, int):
        errors["duration_minutes"] = "Choose a whole number of minutes."
    elif not MIN_DURATION_MINUTES <= minutes <= MAX_DURATION_MINUTES:
        errors["duration_minutes"] = f"Choose between {MIN_DURATION_MINUTES} and {MAX_DURATION_MINUTES} minutes."

    if errors:
        raise ApiError(400, "Please fix the test settings.", "validation_error", errors)
    return count, minutes


def _parse_answer_item(item, index=None):
    where = f" (answer {index + 1})" if index is not None else ""
    if not isinstance(item, dict):
        raise ApiError(400, f"Each answer must be an object{where}.", "validation_error")
    question_id = item.get("question_id")
    option_id = item.get("option_id")
    if isinstance(question_id, bool) or not isinstance(question_id, int):
        raise ApiError(400, f"'question_id' must be a whole number{where}.", "validation_error")
    if option_id is not None and (isinstance(option_id, bool) or not isinstance(option_id, int)):
        raise ApiError(400, f"'option_id' must be a whole number or null{where}.", "validation_error")
    return question_id, option_id


def parse_single_answer(data):
    return _parse_answer_item(data)


def parse_submit(data):
    """Returns {question_id: option_id_or_None}. The answers list is optional (saved answers are used)."""
    answers = data.get("answers", [])
    if not isinstance(answers, list):
        raise ApiError(400, "'answers' must be a list.", "validation_error")
    parsed = {}
    for index, item in enumerate(answers):
        question_id, option_id = _parse_answer_item(item, index)
        if question_id in parsed:
            raise ApiError(400, f"Question {question_id} is answered more than once.", "validation_error")
        parsed[question_id] = option_id
    return parsed
