"""Main Flask application for HTASO Umpire Evaluation system."""
import os
from flask import Flask
from config import config
from models.database import db
from flask_migrate import Migrate


def create_app(config_name=None):
    """Application factory pattern.

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Create tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            # Initialize admin if not exists
            from models.database import Admin
            from utils.auth import init_admin_db
            init_admin_db()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")
            # Continue anyway - will fail later if database is truly unavailable

    # Ensure data directories exist (for legacy JSON and Excel template)
    try:
        app.config['DATA_DIR'].mkdir(parents=True, exist_ok=True)
    except Exception as e:
        app.logger.warning(f"Could not create data directory: {e}")

    # Register blueprints
    from routes.main import main_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Custom template filters
    @app.template_filter('percentage')
    def percentage_filter(value):
        """Format float as percentage."""
        if value is None:
            return "N/A"
        return f"{value * 100:.0f}%"

    @app.template_filter('format_score')
    def format_score_filter(score, possible):
        """Format score as fraction."""
        if possible is None or possible == 0:
            return "0/0"
        return f"{score:.0f}/{possible:.0f}"

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return '<h1>404 - Page Not Found</h1><p>The requested page does not exist.</p>', 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return '<h1>500 - Internal Server Error</h1><p>Something went wrong. Please try again later.</p>', 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8502, debug=True)
