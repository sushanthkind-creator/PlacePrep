from app.extensions import db


class Section(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(40), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    short_name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    topics = db.relationship("Topic", back_populates="section", order_by="Topic.position")

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "short_name": self.short_name,
            "description": self.description,
            "color": self.color,
        }


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False, index=True)
    slug = db.Column(db.String(60), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    section = db.relationship("Section", back_populates="topics")
    lesson = db.relationship("Lesson", back_populates="topic", uselist=False)
    examples = db.relationship("SolvedExample", back_populates="topic", order_by="SolvedExample.position")
    questions = db.relationship("Question", back_populates="topic")

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "summary": self.summary,
            "section_slug": self.section.slug,
        }


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, unique=True)
    # Paragraphs separated by blank lines.
    concept = db.Column(db.Text, nullable=False)
    key_points = db.Column(db.JSON, nullable=False, default=list)
    # [{"label": ..., "formula": ..., "note": ...}]
    formulas = db.Column(db.JSON, nullable=False, default=list)
    tips = db.Column(db.JSON, nullable=False, default=list)

    topic = db.relationship("Topic", back_populates="lesson")

    def to_dict(self):
        return {
            "concept": self.concept,
            "key_points": self.key_points,
            "formulas": self.formulas,
            "tips": self.tips,
        }


class SolvedExample(db.Model):
    __tablename__ = "solved_examples"
    __table_args__ = (db.UniqueConstraint("topic_id", "position", name="uq_example_topic_position"),)

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)
    problem = db.Column(db.Text, nullable=False)
    steps = db.Column(db.JSON, nullable=False, default=list)
    answer = db.Column(db.Text, nullable=False)

    topic = db.relationship("Topic", back_populates="examples")

    def to_dict(self):
        return {"id": self.id, "problem": self.problem, "steps": self.steps, "answer": self.answer}


class Passage(db.Model):
    """Shared text (e.g. a reading comprehension passage) that several questions refer to."""

    __tablename__ = "passages"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), nullable=False, unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "body": self.body}
