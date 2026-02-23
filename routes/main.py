"""Main routes for evaluation form and submission."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, current_app
from datetime import datetime
from pathlib import Path

from utils.excel_parser import load_eval_criteria_from_excel
from utils.export_pdf import generate_pdf_report, get_pdf_filename
from utils.export_word import generate_word_report, get_word_filename
from models.evaluation import (
    RATING_OPTIONS,
    OPTIONAL_NA_LABEL,
    RECOMMENDATION_OPTIONS,
    RECOMMENDATION_COLORS,
    collect_ratings
)
from models.evaluation_service import save_evaluation

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Display the evaluation form."""
    criteria_path = current_app.config['CRITERIA_PATH']
    criteria_structure = load_eval_criteria_from_excel(criteria_path)

    if not criteria_structure:
        flash('Unable to load evaluation criteria from Excel template. Please ensure the file exists and is not open.', 'error')

    return render_template(
        'index.html',
        criteria_structure=criteria_structure,
        rating_options=RATING_OPTIONS,
        optional_na_label=OPTIONAL_NA_LABEL,
        recommendation_options=RECOMMENDATION_OPTIONS,
        recommendation_colors=RECOMMENDATION_COLORS
    )


@main_bp.route('/submit', methods=['POST'])
def submit_evaluation():
    """Process evaluation form submission."""
    # Validate required fields
    evaluator_name = request.form.get('evaluator_name', '').strip()
    trainer_name = request.form.get('trainer_name', '').strip()
    training_date = request.form.get('training_date', '').strip()
    recommendation = request.form.get('recommendation', '').strip()

    errors = []
    if not evaluator_name:
        errors.append('Evaluator Name is required.')
    if not trainer_name:
        errors.append('Trainer Name is required.')
    if not training_date:
        errors.append('Training Date is required.')
    if not recommendation or recommendation == 'Select recommendation':
        errors.append('Overall Recommendation is required.')

    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('main.index'))

    # Collect ratings
    criteria_path = current_app.config['CRITERIA_PATH']
    criteria_structure = load_eval_criteria_from_excel(criteria_path)

    ratings_dict = {}
    rating_details = {}

    for section in criteria_structure:
        for subsection in section.get('subsections', []):
            for item in subsection.get('items', []):
                key = item['key']
                selection = request.form.get(f'rating_{key}', 'Select result')
                ratings_dict[key] = selection
                rating_details[key] = {
                    'section': section['name'],
                    'subsection': subsection['name'],
                    'prompt': item['text']
                }

    # Collect rating summary
    summary = collect_ratings(ratings_dict, rating_details)

    # Build evaluation data
    eval_data = {
        "evaluator_name": evaluator_name,
        "trainer_name": trainer_name,
        "training_date": training_date,
        "observation_date": request.form.get('observation_date', '').strip(),
        "training_location": request.form.get('training_location', '').strip(),
        "eval_type": request.form.get('eval_type', '').strip(),
        "recommendation": recommendation,
        "ratings": summary["entries"],
        "average_score": summary["average"],
        "score_percentage": summary["average"] * 100,
        "rated_item_count": summary["rated_count"],
        "score_counts": summary["score_counts"],
        "section_totals": summary["section_totals"],
        "total_score": summary["total_score"],
        "total_possible": summary["total_possible"],
        "comments": {
            "strengths": request.form.get('strengths', '').strip(),
            "improvement": request.form.get('improvement', '').strip(),
            "development": request.form.get('development', '').strip(),
            "overall": request.form.get('overall', '').strip()
        },
        "submission_date": datetime.now().strftime('%m/%d/%Y %I:%M %p')
    }

    # Save evaluation to database
    saved_eval = save_evaluation(eval_data)

    # Success message
    average_display = f"{summary['average']:.0%}" if summary['total_possible'] else "N/A"
    overall_raw = f"{summary['total_score']:.0f}/{summary['total_possible']}" if summary['total_possible'] else "0/0"

    flash(
        f'Evaluation submitted successfully! '
        f'Evaluator: {evaluator_name}, '
        f'Trainer: {trainer_name}, '
        f'Average Score: {average_display} ({overall_raw}), '
        f'Rated Items: {summary["rated_count"]}',
        'success'
    )

    return redirect(url_for('main.index'))


@main_bp.route('/export/pdf', methods=['POST'])
def export_current_pdf():
    """Export the current form data as PDF (without saving to system)."""
    # Collect form data (similar to submit but don't save)
    evaluator_name = request.form.get('evaluator_name', '').strip()

    if not evaluator_name:
        flash('Please enter Evaluator Name before exporting.', 'error')
        return redirect(url_for('main.index'))

    # Collect all form data
    criteria_path = current_app.config['CRITERIA_PATH']
    criteria_structure = load_eval_criteria_from_excel(criteria_path)

    ratings_dict = {}
    rating_details = {}

    for section in criteria_structure:
        for subsection in section.get('subsections', []):
            for item in subsection.get('items', []):
                key = item['key']
                selection = request.form.get(f'rating_{key}', 'Select result')
                ratings_dict[key] = selection
                rating_details[key] = {
                    'section': section['name'],
                    'subsection': subsection['name'],
                    'prompt': item['text']
                }

    summary = collect_ratings(ratings_dict, rating_details)

    eval_data = {
        "evaluator_name": evaluator_name,
        "trainer_name": request.form.get('trainer_name', '').strip(),
        "training_date": request.form.get('training_date', '').strip(),
        "observation_date": request.form.get('observation_date', '').strip(),
        "training_location": request.form.get('training_location', '').strip(),
        "eval_type": request.form.get('eval_type', '').strip(),
        "recommendation": request.form.get('recommendation', ''),
        "ratings": summary["entries"],
        "average_score": summary["average"],
        "score_percentage": summary["average"] * 100,
        "rated_item_count": summary["rated_count"],
        "score_counts": summary["score_counts"],
        "section_totals": summary["section_totals"],
        "total_score": summary["total_score"],
        "total_possible": summary["total_possible"],
        "comments": {
            "strengths": request.form.get('strengths', '').strip(),
            "improvement": request.form.get('improvement', '').strip(),
            "development": request.form.get('development', '').strip(),
            "overall": request.form.get('overall', '').strip()
        },
        "submission_date": datetime.now().strftime('%m/%d/%Y %I:%M %p')
    }

    # Generate PDF
    logo_path = current_app.config['LOGO_PATH']
    pdf_buffer = generate_pdf_report(eval_data, logo_path)
    filename = get_pdf_filename(evaluator_name)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@main_bp.route('/export/word', methods=['POST'])
def export_current_word():
    """Export the current form data as Word document (without saving to system)."""
    # Collect form data (similar to submit but don't save)
    evaluator_name = request.form.get('evaluator_name', '').strip()

    if not evaluator_name:
        flash('Please enter Evaluator Name before exporting.', 'error')
        return redirect(url_for('main.index'))

    # Collect all form data
    criteria_path = current_app.config['CRITERIA_PATH']
    criteria_structure = load_eval_criteria_from_excel(criteria_path)

    ratings_dict = {}
    rating_details = {}

    for section in criteria_structure:
        for subsection in section.get('subsections', []):
            for item in subsection.get('items', []):
                key = item['key']
                selection = request.form.get(f'rating_{key}', 'Select result')
                ratings_dict[key] = selection
                rating_details[key] = {
                    'section': section['name'],
                    'subsection': subsection['name'],
                    'prompt': item['text']
                }

    summary = collect_ratings(ratings_dict, rating_details)

    eval_data = {
        "evaluator_name": evaluator_name,
        "trainer_name": request.form.get('trainer_name', '').strip(),
        "training_date": request.form.get('training_date', '').strip(),
        "observation_date": request.form.get('observation_date', '').strip(),
        "training_location": request.form.get('training_location', '').strip(),
        "eval_type": request.form.get('eval_type', '').strip(),
        "recommendation": request.form.get('recommendation', ''),
        "ratings": summary["entries"],
        "average_score": summary["average"],
        "score_percentage": summary["average"] * 100,
        "rated_item_count": summary["rated_count"],
        "score_counts": summary["score_counts"],
        "section_totals": summary["section_totals"],
        "total_score": summary["total_score"],
        "total_possible": summary["total_possible"],
        "comments": {
            "strengths": request.form.get('strengths', '').strip(),
            "improvement": request.form.get('improvement', '').strip(),
            "development": request.form.get('development', '').strip(),
            "overall": request.form.get('overall', '').strip()
        },
        "submission_date": datetime.now().strftime('%m/%d/%Y %I:%M %p')
    }

    # Generate Word document
    logo_path = current_app.config['LOGO_PATH']
    word_buffer = generate_word_report(eval_data, logo_path)
    filename = get_word_filename(evaluator_name)

    return send_file(
        word_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
