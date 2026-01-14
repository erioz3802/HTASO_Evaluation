"""Database models for PostgreSQL storage."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()


class Admin(db.Model):
    """Admin authentication table."""
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.id}>'


class Evaluation(db.Model):
    """Evaluation submissions table."""
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)

    # Basic information
    evaluator_name = db.Column(db.String(200), nullable=False, index=True)
    trainer_name = db.Column(db.String(200), nullable=False, index=True)
    training_date = db.Column(db.String(50), nullable=False)
    observation_date = db.Column(db.String(50))
    training_location = db.Column(db.String(200))
    eval_type = db.Column(db.String(200))

    # Recommendation
    recommendation = db.Column(db.String(200), nullable=False)

    # Ratings (stored as JSON array)
    ratings = db.Column(JSON, nullable=False)

    # Scores
    average_score = db.Column(db.Float, default=0.0)
    score_percentage = db.Column(db.Float, default=0.0)
    rated_item_count = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Float, default=0.0)
    total_possible = db.Column(db.Float, default=0.0)

    # Score counts and section totals (stored as JSON)
    score_counts = db.Column(JSON)
    section_totals = db.Column(JSON)

    # Comments (stored as JSON object)
    comments = db.Column(JSON)

    # Metadata
    submission_date = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Evaluation {self.id}: {self.evaluator_name} by {self.trainer_name}>'

    def to_dict(self):
        """Convert evaluation to dictionary format (compatible with JSON format)."""
        return {
            'id': self.id,
            'evaluator_name': self.evaluator_name,
            'trainer_name': self.trainer_name,
            'training_date': self.training_date,
            'observation_date': self.observation_date,
            'training_location': self.training_location,
            'eval_type': self.eval_type,
            'recommendation': self.recommendation,
            'ratings': self.ratings,
            'average_score': self.average_score,
            'score_percentage': self.score_percentage,
            'rated_item_count': self.rated_item_count,
            'total_score': self.total_score,
            'total_possible': self.total_possible,
            'score_counts': self.score_counts,
            'section_totals': self.section_totals,
            'comments': self.comments,
            'submission_date': self.submission_date,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
