from datetime import datetime, timezone


def utcnow():
    """Naive UTC timestamp. SQLite drops timezone info, so every stored time is naive UTC."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def iso(value):
    """Serialise a naive UTC datetime as ISO 8601 with a Z suffix."""
    return value.isoformat(timespec="seconds") + "Z" if value else None
