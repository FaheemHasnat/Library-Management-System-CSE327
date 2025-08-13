from flask import Flask, render_template, redirect, url_for, session
from config import config_by_name
import logging
import os


def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    
    config_class = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_class)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    
    from app.controllers.user_controller import user_bp
    from app.controllers.dashboard_controller import dashboard_bp
<<<<<<< HEAD
    from app.controllers.reservation_controller import reservation_bp
    from app.controllers.search_controller import search_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(search_bp)
=======
    
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    
    @app.route('/')
    def index():
        if session.get('logged_in'):
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('user.login'))
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('404.html'), 500
    
    @app.template_filter('datetime_format')
    def datetime_format(value, format='%Y-%m-%d %H:%M'):
        if value is None:
            return ""
        return value.strftime(format)
    
    @app.template_filter('date_format')
    def date_format(value, format='%Y-%m-%d'):
        if value is None:
            return ""
        return value.strftime(format)
    
    @app.context_processor
    def inject_user():
        return {
            'current_user': {
                'id': session.get('user_id'),
                'name': session.get('user_name'),
                'email': session.get('user_email'),
                'role': session.get('user_role'),
                'logged_in': session.get('logged_in', False)
            }
        }
    
    return app


if __name__ == '__main__':
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', False)
    )
