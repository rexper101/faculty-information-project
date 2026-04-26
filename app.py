from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.departments import departments_bp
    from routes.faculty import faculty_bp
    from routes.qualifications import qualifications_bp
    from routes.experience import experience_bp
    from routes.documents import documents_bp
    from routes.publications import publications_bp
    from routes.performance import performance_bp
    from routes.salary import salary_bp
    from routes.attendance import attendance_bp
    from routes.leaves import leaves_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(qualifications_bp)
    app.register_blueprint(experience_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(publications_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leaves_bp)

    # ── Context processors ────────────────────────────────────────────
    from datetime import datetime as _dt

    @app.context_processor
    def inject_globals():
        try:
            from models.models import AdminUser
            setup_avail = AdminUser.query.count() == 0
        except Exception:
            setup_avail = False
        return {
            'now': _dt.utcnow(),
            'setup_available': setup_avail,
        }

    # ── Error handlers ─────────────────────────────────────────────────
    from flask import render_template as _rt

    @app.errorhandler(404)
    def not_found(e):
        return _rt('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return _rt('errors/500.html'), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
