from app.extensions import db
from app.utils.errors import error_response


def register_jwt_handlers(jwt):
    from app.models import RevokedToken, User

    @jwt.user_lookup_loader
    def load_user(_header, payload):
        try:
            return db.session.get(User, int(payload["sub"]))
        except (TypeError, ValueError):
            return None

    @jwt.token_in_blocklist_loader
    def is_revoked(_header, payload):
        return db.session.query(RevokedToken.id).filter_by(jti=payload["jti"]).first() is not None

    @jwt.user_lookup_error_loader
    def user_missing(_header, _payload):
        return error_response(401, "Your account could not be found. Please log in again.", "invalid_token")

    @jwt.expired_token_loader
    def expired(_header, _payload):
        return error_response(401, "Your session has expired. Please log in again.", "token_expired")

    @jwt.invalid_token_loader
    def invalid(_reason):
        return error_response(401, "Your session is invalid. Please log in again.", "invalid_token")

    @jwt.unauthorized_loader
    def missing(_reason):
        return error_response(401, "Please log in to continue.", "auth_required")

    @jwt.revoked_token_loader
    def revoked(_header, _payload):
        return error_response(401, "You have logged out. Please log in again.", "token_revoked")
