"""Admin routes for authentication and evaluation management."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, send_file, current_app
from pathlib import Path

from utils.auth import verify_admin_password_db, update_admin_password_db, admin_required
from utils.export_pdf import generate_pdf_report, get_pdf_filename
from utils.export_word import generate_word_report, get_word_filename
from models.evaluation_service import list_evaluations, get_evaluation, get_all_trainers

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    # If already logged in, redirect to dashboard
    if session.get('admin_authenticated'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        password = request.form.get('password', '')

        if verify_admin_password_db(password):
            session['admin_authenticated'] = True
            session.permanent = True  # Use permanent session lifetime
            flash('Welcome to the admin panel!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid password. Please try again.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    """Admin logout."""
    session.pop('admin_authenticated', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard showing all evaluations."""
    # Get filter parameter
    filter_trainer = request.args.get('trainer', '')

    # Get evaluations (filtered if trainer specified)
    evaluations = list_evaluations(filter_trainer if filter_trainer else None)

    # Get unique trainers for filter dropdown
    trainers = get_all_trainers()

    return render_template(
        'admin/dashboard.html',
        evaluations=evaluations,
        trainers=trainers,
        filter_trainer=filter_trainer
    )


@admin_bp.route('/evaluation/<int:eval_id>')
@admin_required
def evaluation_detail(eval_id):
    """View detailed evaluation information.

    Args:
        eval_id: Evaluation ID
    """
    # Load evaluation from database
    evaluation = get_evaluation(eval_id)
    if not evaluation:
        flash('Evaluation not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/detail.html', evaluation=evaluation, eval_id=eval_id)


@admin_bp.route('/export/<int:eval_id>/pdf')
@admin_required
def export_evaluation_pdf(eval_id):
    """Export stored evaluation as PDF.

    Args:
        eval_id: Evaluation ID
    """
    # Load evaluation from database
    evaluation = get_evaluation(eval_id)
    if not evaluation:
        flash('Evaluation not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    # Generate PDF
    logo_path = current_app.config['LOGO_PATH']
    pdf_buffer = generate_pdf_report(evaluation, logo_path)
    filename = get_pdf_filename(evaluation.get('evaluator_name', 'Evaluation'))

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@admin_bp.route('/export/<int:eval_id>/word')
@admin_required
def export_evaluation_word(eval_id):
    """Export stored evaluation as Word document.

    Args:
        eval_id: Evaluation ID
    """
    # Load evaluation from database
    evaluation = get_evaluation(eval_id)
    if not evaluation:
        flash('Evaluation not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    # Generate Word document
    logo_path = current_app.config['LOGO_PATH']
    word_buffer = generate_word_report(evaluation, logo_path)
    filename = get_word_filename(evaluation.get('evaluator_name', 'Evaluation'))

    return send_file(
        word_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@admin_bp.route('/change-password', methods=['POST'])
@admin_required
def change_password():
    """Change admin password."""
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    # Validate current password
    if not verify_admin_password_db(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('admin.dashboard'))

    # Validate new passwords match
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('admin.dashboard'))

    # Validate minimum length
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return redirect(url_for('admin.dashboard'))

    # Update password
    if update_admin_password_db(new_password):
        flash('Password changed successfully!', 'success')
    else:
        flash('Failed to update password. Please try again.', 'error')

    return redirect(url_for('admin.dashboard'))
