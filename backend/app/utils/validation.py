import re

from flask import request

from app.utils.errors import ApiError

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$")
# Indian mobile numbers: 10 digits starting 6-9, optionally prefixed with +91, 91 or 0.
MOBILE_RE = re.compile(r"^(?:\+?91|0)?([6-9]\d{9})$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'\-]*$")


def get_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError(400, "Send the request body as a JSON object.", "invalid_body")
    return data


def clean_str(value):
    return value.strip() if isinstance(value, str) else ""


def normalize_email(value):
    return clean_str(value).lower()


def validate_email(value):
    email = normalize_email(value)
    if not email:
        return email, "Enter your college email ID."
    if len(email) > 254 or not EMAIL_RE.match(email):
        return email, "Enter a valid email address, like name@college.edu."
    return email, None


def validate_mobile(value):
    raw = re.sub(r"[\s\-()]", "", clean_str(value))
    if not raw:
        return "", "Enter your mobile number."
    match = MOBILE_RE.match(raw)
    if not match:
        return raw, "Enter a valid 10-digit Indian mobile number starting with 6, 7, 8 or 9."
    return match.group(1), None


def validate_full_name(value):
    name = re.sub(r"\s+", " ", clean_str(value))
    if not name:
        return name, "Enter your full name."
    if len(name) < 2 or len(name) > 100:
        return name, "Name must be between 2 and 100 characters."
    if not NAME_RE.match(name):
        return name, "Name can contain only letters, spaces, dots, hyphens and apostrophes."
    return name, None


def validate_college_name(value):
    college = re.sub(r"\s+", " ", clean_str(value))
    if not college:
        return college, "Enter your college name."
    if len(college) < 2 or len(college) > 150:
        return college, "College name must be between 2 and 150 characters."
    return college, None


def validate_new_password(password, confirm):
    if not isinstance(password, str) or not password:
        return "Enter a password."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if len(password) > 128:
        return "Password must be at most 128 characters."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password must contain at least one letter and one number."
    if confirm is not None and password != confirm:
        return "Passwords do not match."
    return None


def require_int(value, field):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ApiError(400, f"'{field}' must be a whole number.", "validation_error", {field: "Must be a whole number."})
    return value
