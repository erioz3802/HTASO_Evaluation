"""Authentication utilities for admin access."""
import hashlib
import json
from pathlib import Path
from functools import wraps
from flask import session, redirect, url_for, flash, current_app
from models.database import db, Admin


def init_admin(admin_config_path: Path) -> None:
    """Initialize admin configuration with default password if not exists.

    Default password: admin123

    Args:
        admin_config_path: Path to admin_config.json file
    """
    # Create parent directory if needed
    admin_config_path.parent.mkdir(parents=True, exist_ok=True)

    if not admin_config_path.exists():
        # Default password: admin123
        default_hash = hashlib.sha256("admin123".encode()).hexdigest()
        with open(admin_config_path, 'w') as f:
            json.dump({"password_hash": default_hash}, f)


def verify_admin_password(password: str, admin_config_path: Path) -> bool:
    """Verify admin password against stored hash.

    Args:
        password: Password to verify
        admin_config_path: Path to admin_config.json file

    Returns:
        True if password matches, False otherwise
    """
    if not admin_config_path.exists():
        return False

    try:
        with open(admin_config_path, 'r') as f:
            config = json.load(f)

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == config.get("password_hash")
    except Exception:
        return False


def update_admin_password(new_password: str, admin_config_path: Path) -> bool:
    """Update admin password.

    Args:
        new_password: New password to set
        admin_config_path: Path to admin_config.json file

    Returns:
        True if successful, False otherwise
    """
    try:
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        with open(admin_config_path, 'w') as f:
            json.dump({"password_hash": new_hash}, f)
        return True
    except Exception:
        return False


def admin_required(f):
    """Decorator to require admin authentication for a route.

    Usage:
        @app.route('/admin/dashboard')
        @admin_required
        def admin_dashboard():
            return render_template('admin/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


# Database authentication functions

def init_admin_db() -> None:
    """Initialize admin in database with default password if not exists.

    Default password: admin123
    """
    admin = Admin.query.first()
    if not admin:
        default_hash = hashlib.sha256("admin123".encode()).hexdigest()
        admin = Admin(password_hash=default_hash)
        db.session.add(admin)
        db.session.commit()


def verify_admin_password_db(password: str) -> bool:
    """Verify admin password against database.

    Args:
        password: Password to verify

    Returns:
        True if password matches, False otherwise
    """
    try:
        admin = Admin.query.first()
        if not admin:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == admin.password_hash
    except Exception:
        return False


def update_admin_password_db(new_password: str) -> bool:
    """Update admin password in database.

    Args:
        new_password: New password to set

    Returns:
        True if successful, False otherwise
    """
    try:
        admin = Admin.query.first()
        if not admin:
            admin = Admin()
            db.session.add(admin)

        admin.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
