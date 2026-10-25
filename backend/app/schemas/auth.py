from app.utils.errors import ApiError
from app.utils.validation import (
    normalize_email,
    validate_college_name,
    validate_email,
    validate_full_name,
    validate_mobile,
    validate_new_password,
)

FIX_FIELDS = "Please fix the highlighted fields."


def parse_register(data):
    errors = {}
    full_name, err = validate_full_name(data.get("full_name"))
    if err:
        errors["full_name"] = err
    mobile, err = validate_mobile(data.get("mobile"))
    if err:
        errors["mobile"] = err
    email, err = validate_email(data.get("email"))
    if err:
        errors["email"] = err
    college_name, err = validate_college_name(data.get("college_name"))
    if err:
        errors["college_name"] = err

    password = data.get("password")
    confirm = data.get("confirm_password")
    err = validate_new_password(password, None)
    if err:
        errors["password"] = err
    if not isinstance(confirm, str) or not confirm:
        errors["confirm_password"] = "Confirm your password."
    elif not err and confirm != password:
        errors["confirm_password"] = "Passwords do not match."

    if errors:
        raise ApiError(400, FIX_FIELDS, "validation_error", errors)
    return {
        "full_name": full_name,
        "mobile": mobile,
        "email": email,
        "college_name": college_name,
        "password": password,
    }


def parse_login(data):
    email = normalize_email(data.get("email"))
    password = data.get("password")
    errors = {}
    if not email:
        errors["email"] = "Enter your college email ID."
    if not isinstance(password, str) or not password:
        errors["password"] = "Enter your password."
    if errors:
        raise ApiError(400, FIX_FIELDS, "validation_error", errors)
    return email, password


def parse_profile_update(data):
    if "email" in data:
        raise ApiError(400, FIX_FIELDS, "validation_error", {"email": "Your email is your login ID and can't be changed."})

    validators = {
        "full_name": validate_full_name,
        "mobile": validate_mobile,
        "college_name": validate_college_name,
    }
    updates, errors = {}, {}
    for field, validator in validators.items():
        if field in data:
            value, err = validator(data[field])
            if err:
                errors[field] = err
            else:
                updates[field] = value
    if errors:
        raise ApiError(400, FIX_FIELDS, "validation_error", errors)
    if not updates:
        raise ApiError(400, "Nothing to update. Send full_name, mobile or college_name.", "validation_error")
    return updates


def parse_password_change(data, user):
    errors = {}
    current = data.get("current_password")
    if user.password_hash and not (isinstance(current, str) and current):
        errors["current_password"] = "Enter your current password."
    err = validate_new_password(data.get("new_password"), data.get("confirm_password"))
    if err:
        key = "confirm_password" if err == "Passwords do not match." else "new_password"
        errors[key] = err
    if errors:
        raise ApiError(400, FIX_FIELDS, "validation_error", errors)
    return current, data["new_password"]
