import logging

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Raised by route code to return a consistent JSON error."""

    def __init__(self, status, message, code="error", fields=None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.code = code
        self.fields = fields or None


def error_response(status, message, code="error", fields=None):
    body = {"error": {"code": code, "message": message}}
    if fields:
        body["error"]["fields"] = fields
    return jsonify(body), status


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err):
        return error_response(err.status, err.message, err.code, err.fields)

    @app.errorhandler(HTTPException)
    def handle_http_error(err):
        messages = {
            400: ("bad_request", "The request could not be understood."),
            404: ("not_found", "The requested resource was not found."),
            405: ("method_not_allowed", "This method is not allowed for this URL."),
            415: ("unsupported_media_type", "Send the request body as JSON."),
        }
        code, message = messages.get(err.code, ("error", err.description or "Request failed."))
        return error_response(err.code, message, code)

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        # Log the path only; request bodies may contain passwords.
        logger.exception("Unhandled error on %s %s", request.method, request.path)
        return error_response(500, "Something went wrong on the server. Please try again.", "server_error")
