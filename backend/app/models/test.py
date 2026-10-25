from app.extensions import db
from app.utils.time import utcnow

SCOPE_TOPIC = "topic"
SCOPE_SECTION = "section"
SCOPE_MIXED = "mixed"

STATUS_IN_PROGRESS = "in_progress"
STATUS_SUBMITTED = "submitted"


class TestDefinition(db.Model):
    __test__ = False  # not a pytest test class
    __tablename__ = "test_definitions"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    scope = db.Column(db.String(10), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=True, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=True, index=True)
    default_question_count = db.Column(db.Integer, nullable=False)
    default_duration_minutes = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    section = db.relationship("Section")
    topic = db.relationship("Topic")


class TestAttempt(db.Model):
    __test__ = False
    __tablename__ = "test_attempts"
    __table_args__ = (db.Index("ix_attempts_user_status", "user_id", "status"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("test_definitions.id"), nullable=False, index=True)
    status = db.Column(db.String(12), nullable=False, default=STATUS_IN_PROGRESS)
    question_count = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    auto_submitted = db.Column(db.Boolean, nullable=False, default=False)
    correct_count = db.Column(db.Integer, nullable=True)
    incorrect_count = db.Column(db.Integer, nullable=True)
    unanswered_count = db.Column(db.Integer, nullable=True)
    percentage = db.Column(db.Float, nullable=True)
    time_taken_seconds = db.Column(db.Integer, nullable=True)

    test = db.relationship("TestDefinition")
    questions = db.relationship(
        "AttemptQuestion", back_populates="attempt", order_by="AttemptQuestion.position", cascade="all, delete-orphan"
    )


class AttemptQuestion(db.Model):
    """A question drawn into an attempt, and the student's saved answer."""

    __tablename__ = "attempt_questions"
    __table_args__ = (
        db.UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question"),
        db.UniqueConstraint("attempt_id", "position", name="uq_attempt_position"),
    )

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("test_attempts.id"), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey("answer_options.id"), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)

    attempt = db.relationship("TestAttempt", back_populates="questions")
    question = db.relationship("Question")
