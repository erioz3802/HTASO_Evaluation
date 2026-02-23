"""Evaluation data model and business logic."""
import json
import copy
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


# Rating scale definition (HTASO scale: 1=best, 5=worst)
# Internal scores are inverted so higher = better for calculations
RATING_SCALE = [
    ("1 - Outstanding", 5),
    ("2 - Above Standard", 4),
    ("3 - Meets Standard", 3),
    ("4 - Below Standard", 2),
    ("5 - Unsatisfactory", 1),
]

OPTIONAL_NA_LABEL = "Not Observed"
RATING_OPTIONS = [label for label, _ in RATING_SCALE]
RATING_VALUE_MAP = {label: score for label, score in RATING_SCALE}
RATING_VALUE_MAP[OPTIONAL_NA_LABEL] = None

# Recommendation options
RECOMMENDATION_OPTIONS = [
    "Approved for Independent Evaluation",
    "Approved with Additional Training Required",
    "Requires Further Training Before Approval",
    "Not Approved - Significant Concerns"
]

# Recommendation colors for display
RECOMMENDATION_COLORS = {
    "Approved for Independent Evaluation": "#2A9D8F",  # Secondary (green)
    "Approved with Additional Training Required": "#F4A261",  # Orange
    "Requires Further Training Before Approval": "#F97316",  # Dark orange
    "Not Approved - Significant Concerns": "#E76F51"  # Accent (red)
}


def compute_section_summary(ratings: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], float, float]:
    """Calculate per-section and overall scores from rating entries.

    Args:
        ratings: List of rating dictionaries with section, score, etc.

    Returns:
        Tuple of (section_list, total_score, total_possible)
    """
    totals = OrderedDict()
    total_score = 0.0
    total_possible = 0.0

    for item in ratings:
        section = item.get("section") or "General"
        score = item.get("score")

        # Convert string scores to float
        if isinstance(score, str):
            try:
                score = float(score)
            except ValueError:
                score = None

        if not isinstance(score, (int, float)):
            score = None

        # Initialize section if not exists
        if section not in totals:
            totals[section] = {"score": 0.0, "count": 0}

        # Add score if valid
        if score is not None and score > 0:
            totals[section]["score"] += score
            totals[section]["count"] += 1
            total_score += score
            total_possible += 5  # Max score per item

    # Build section list
    section_list = []
    for section, data in totals.items():
        possible = data["count"] * 5
        percentage = (data["score"] / possible) if possible else 0.0
        section_list.append({
            "section": section,
            "score": data["score"],
            "possible": possible,
            "percentage": percentage
        })

    return section_list, total_score, total_possible


def collect_ratings(ratings_dict: Dict[str, str], rating_details: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    """Gather current rating selections with summary statistics.

    Args:
        ratings_dict: Dictionary of {key: selection_label}
        rating_details: Dictionary of {key: {section, subsection, prompt}}

    Returns:
        Dictionary with entries, average, counts, section totals, etc.
    """
    rating_entries = []
    score_counts = {label: 0 for label in RATING_VALUE_MAP.keys()}
    rated_items = 0

    for key, selection in ratings_dict.items():
        if selection == "Select result" or not selection:
            selection = None

        detail = rating_details.get(key, {})
        score_value = RATING_VALUE_MAP.get(selection) if selection else None

        if selection and selection in score_counts:
            score_counts[selection] += 1

        if score_value is not None:
            rated_items += 1

        rating_entries.append({
            "key": key,
            "section": detail.get("section"),
            "subsection": detail.get("subsection"),
            "prompt": detail.get("prompt"),
            "selection": selection,
            "score": score_value
        })

    # Compute section summaries
    section_totals, total_score, total_possible = compute_section_summary(rating_entries)
    average_score = (total_score / total_possible) if total_possible else 0.0

    # Build summary section totals
    summary_section_totals = [
        {
            "section": entry["section"],
            "score": entry["score"],
            "possible": entry["possible"],
            "percentage": entry["percentage"]
        }
        for entry in section_totals
    ]

    return {
        "entries": rating_entries,
        "average": average_score,
        "rated_count": rated_items,
        "score_counts": score_counts,
        "section_totals": summary_section_totals,
        "total_score": total_score,
        "total_possible": total_possible
    }


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()


def save_evaluation(data: Dict[str, Any], data_dir: Path) -> Path:
    """Save evaluation to JSON file.

    Args:
        data: Evaluation data dictionary
        data_dir: Root data directory

    Returns:
        Path to saved file
    """
    # Create trainer directory
    trainer_name = data.get("trainer_name", "Unknown")
    trainer_dir = data_dir / sanitize_filename(trainer_name)
    trainer_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    evaluator_name = data.get("evaluator_name", "Unknown")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{sanitize_filename(evaluator_name)}_{timestamp}.json"
    filepath = trainer_dir / filename

    # Save JSON
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return filepath


def list_evaluations(data_dir: Path) -> List[Dict[str, Any]]:
    """List all evaluation submissions.

    Args:
        data_dir: Root data directory

    Returns:
        List of evaluation metadata dictionaries
    """
    evaluations = []

    if not data_dir.exists():
        return evaluations

    # Iterate through trainer directories
    for trainer_dir in sorted(data_dir.iterdir()):
        if not trainer_dir.is_dir() or trainer_dir.name in ['__pycache__']:
            continue

        # Iterate through JSON files
        for filepath in sorted(trainer_dir.glob("*.json"), reverse=True):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)

                evaluations.append({
                    "filepath": filepath,
                    "trainer": trainer_dir.name,
                    "evaluator": data.get("evaluator_name", "Unknown"),
                    "training_date": data.get("training_date", "N/A"),
                    "submission_date": data.get("submission_date", "N/A"),
                    "average": data.get("average_score", 0.0),
                    "total_score": data.get("total_score", 0.0),
                    "total_possible": data.get("total_possible", 0.0),
                    "recommendation": data.get("recommendation", "Not Selected")
                })
            except Exception:
                # Skip malformed files
                continue

    return evaluations


def get_evaluation(filepath: Path) -> Optional[Dict[str, Any]]:
    """Load a single evaluation from file.

    Args:
        filepath: Path to evaluation JSON file

    Returns:
        Evaluation data dictionary or None if not found
    """
    if not filepath.exists():
        return None

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return normalize_evaluation_data(data)
    except Exception:
        return None


def normalize_evaluation_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure legacy evaluation records conform to the current data structure.

    Args:
        data: Raw evaluation data

    Returns:
        Normalized evaluation data
    """
    normalized = copy.deepcopy(data)

    # Normalize ratings format
    ratings = normalized.get("ratings", [])
    if isinstance(ratings, dict):
        # Convert old dict format to list
        converted = []
        for key, value in ratings.items():
            converted.append({
                "key": key,
                "section": "Legacy",
                "subsection": "Criteria",
                "prompt": key.replace('_', ' ').title(),
                "selection": f"{value}/5" if isinstance(value, (int, float)) else value,
                "score": value if isinstance(value, (int, float)) else None
            })
        normalized["ratings"] = converted
    elif not isinstance(ratings, list):
        normalized["ratings"] = []

    # Normalize average score
    avg = normalized.get("average_score")
    if isinstance(avg, (int, float)):
        # Legacy values were stored on a 0-5 scale
        if avg > 1.5:
            normalized["average_score"] = avg / 5
    else:
        normalized["average_score"] = 0.0

    # Recalculate section totals
    section_totals, total_score, total_possible = compute_section_summary(normalized.get("ratings", []))
    normalized["section_totals"] = section_totals
    normalized["total_score"] = total_score
    normalized["total_possible"] = total_possible

    if total_possible:
        normalized["average_score"] = total_score / total_possible

    normalized["score_percentage"] = normalized.get("average_score", 0.0) * 100
    normalized["rated_item_count"] = sum(
        int(entry.get("possible", 0) / 5) for entry in section_totals
    )

    # Normalize score counts
    counts = normalized.get("score_counts") or {}
    for label in RATING_VALUE_MAP.keys():
        counts.setdefault(label, 0)
    normalized["score_counts"] = counts

    return normalized


def format_datetime_display(value: str, include_time: bool = True) -> str:
    """Convert a stored datetime string into MM/DD/YYYY format.

    Args:
        value: Datetime string
        include_time: Whether to include time in output

    Returns:
        Formatted datetime string or "N/A" if invalid
    """
    if not value:
        return "N/A"

    patterns = [
        "%m/%d/%Y %I:%M %p",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d"
    ]

    for pattern in patterns:
        try:
            dt = datetime.strptime(value, pattern)
            if include_time:
                return dt.strftime("%m/%d/%Y %I:%M %p")
            else:
                return dt.strftime("%m/%d/%Y")
        except ValueError:
            continue

    return value
