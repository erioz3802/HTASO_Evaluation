"""Service layer for evaluation database operations."""
from typing import List, Dict, Any, Optional
from models.database import db, Evaluation
from models.evaluation import (
    RATING_SCALE,
    OPTIONAL_NA_LABEL,
    RATING_OPTIONS,
    RATING_VALUE_MAP,
    RECOMMENDATION_OPTIONS,
    compute_section_summary
)


def save_evaluation(data: Dict[str, Any]) -> Evaluation:
    """Save evaluation to database.

    Args:
        data: Evaluation data dictionary

    Returns:
        Saved Evaluation model instance
    """
    evaluation = Evaluation(
        evaluator_name=data.get('evaluator_name'),
        trainer_name=data.get('trainer_name'),
        training_date=data.get('training_date'),
        observation_date=data.get('observation_date'),
        training_location=data.get('training_location'),
        eval_type=data.get('eval_type'),
        recommendation=data.get('recommendation'),
        ratings=data.get('ratings', []),
        average_score=data.get('average_score', 0.0),
        score_percentage=data.get('score_percentage', 0.0),
        rated_item_count=data.get('rated_item_count', 0),
        total_score=data.get('total_score', 0.0),
        total_possible=data.get('total_possible', 0.0),
        score_counts=data.get('score_counts', {}),
        section_totals=data.get('section_totals', []),
        comments=data.get('comments', {}),
        submission_date=data.get('submission_date')
    )

    db.session.add(evaluation)
    db.session.commit()

    return evaluation


def list_evaluations(trainer_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all evaluation submissions.

    Args:
        trainer_name: Optional trainer name to filter by

    Returns:
        List of evaluation metadata dictionaries
    """
    query = Evaluation.query

    if trainer_name and trainer_name != 'all':
        query = query.filter_by(trainer_name=trainer_name)

    evaluations = query.order_by(Evaluation.created_at.desc()).all()

    return [
        {
            'id': eval.id,
            'trainer': eval.trainer_name,
            'evaluator': eval.evaluator_name,
            'training_date': eval.training_date,
            'submission_date': eval.submission_date,
            'average': eval.average_score,
            'total_score': eval.total_score,
            'total_possible': eval.total_possible,
            'recommendation': eval.recommendation,
            'created_at': eval.created_at
        }
        for eval in evaluations
    ]


def get_evaluation(evaluation_id: int) -> Optional[Dict[str, Any]]:
    """Get a single evaluation by ID.

    Args:
        evaluation_id: Evaluation ID

    Returns:
        Evaluation dictionary or None if not found
    """
    evaluation = Evaluation.query.get(evaluation_id)

    if not evaluation:
        return None

    return evaluation.to_dict()


def get_all_trainers() -> List[str]:
    """Get list of all unique trainer names.

    Returns:
        List of trainer names
    """
    trainers = db.session.query(Evaluation.trainer_name).distinct().order_by(Evaluation.trainer_name).all()
    return [trainer[0] for trainer in trainers]


def search_evaluations(
    evaluator_name: Optional[str] = None,
    trainer_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search evaluations with filters.

    Args:
        evaluator_name: Filter by evaluator name (partial match)
        trainer_name: Filter by trainer name (exact match)
        start_date: Filter by start date
        end_date: Filter by end date

    Returns:
        List of matching evaluations
    """
    query = Evaluation.query

    if evaluator_name:
        query = query.filter(Evaluation.evaluator_name.ilike(f'%{evaluator_name}%'))

    if trainer_name and trainer_name != 'all':
        query = query.filter_by(trainer_name=trainer_name)

    if start_date:
        query = query.filter(Evaluation.training_date >= start_date)

    if end_date:
        query = query.filter(Evaluation.training_date <= end_date)

    evaluations = query.order_by(Evaluation.created_at.desc()).all()

    return [eval.to_dict() for eval in evaluations]


def delete_evaluation(evaluation_id: int) -> bool:
    """Delete an evaluation.

    Args:
        evaluation_id: Evaluation ID to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        evaluation = Evaluation.query.get(evaluation_id)
        if evaluation:
            db.session.delete(evaluation)
            db.session.commit()
            return True
        return False
    except Exception:
        db.session.rollback()
        return False


def get_evaluation_stats() -> Dict[str, Any]:
    """Get overall statistics.

    Returns:
        Dictionary with statistics
    """
    total_evaluations = Evaluation.query.count()
    total_trainers = db.session.query(Evaluation.trainer_name).distinct().count()
    total_evaluators = db.session.query(Evaluation.evaluator_name).distinct().count()

    avg_score = db.session.query(db.func.avg(Evaluation.average_score)).scalar() or 0.0

    return {
        'total_evaluations': total_evaluations,
        'total_trainers': total_trainers,
        'total_evaluators': total_evaluators,
        'average_score': float(avg_score)
    }
