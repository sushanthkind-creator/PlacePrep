from app.extensions import db

POOL_PRACTICE = "practice"
POOL_TEST = "test"


class Question(db.Model):
    __tablename__ = "questions"
    __table_args__ = (db.Index("ix_questions_topic_pool", "topic_id", "pool"),)

    id = db.Column(db.Integer, primary_key=True)
    # Stable identifier from the seed content, so re-seeding updates rather than duplicates.
    seed_key = db.Column(db.String(80), nullable=False, unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    passage_id = db.Column(db.Integer, db.ForeignKey("passages.id"), nullable=True)
    pool = db.Column(db.String(10), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    prompt = db.Column(db.Text, nullable=False)
    # Optional data table: {"columns": [...], "rows": [[...], ...], "caption": "..."}
    table = db.Column(db.JSON, nullable=True)
    explanation = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False, default="medium")

    topic = db.relationship("Topic", back_populates="questions")
    passage = db.relationship("Passage")
    options = db.relationship(
        "AnswerOption", back_populates="question", order_by="AnswerOption.label", cascade="all, delete-orphan"
    )

    @property
    def correct_option(self):
        return next((o for o in self.options if o.is_correct), None)

    def to_public_dict(self):
        """Question as shown to a student: no answer key, no explanation."""
        return {
            "id": self.id,
            "prompt": self.prompt,
            "table": self.table,
            "passage": self.passage.to_dict() if self.passage else None,
            "difficulty": self.difficulty,
            "topic": {"slug": self.topic.slug, "name": self.topic.name},
            "options": [{"id": o.id, "label": o.label, "text": o.text} for o in self.options],
        }


class AnswerOption(db.Model):
    __tablename__ = "answer_options"
    __table_args__ = (db.UniqueConstraint("question_id", "label", name="uq_option_question_label"),)

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    label = db.Column(db.String(1), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship("Question", back_populates="options")
