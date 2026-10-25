from app.extensions import db
from app.utils.time import utcnow


class TopicProgress(db.Model):
    __tablename__ = "topic_progress"
    __table_args__ = (db.UniqueConstraint("user_id", "topic_id", name="uq_progress_user_topic"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    last_viewed_at = db.Column(db.DateTime, nullable=True)


class PracticeAnswer(db.Model):
    """Every 'Check answer' on a practice question. The latest one per question counts for stats."""

    __tablename__ = "practice_answers"
    __table_args__ = (db.Index("ix_practice_user_question", "user_id", "question_id"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey("answer_options.id"), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False, default=utcnow)
