from flask import Flask
from config import Config


def create_app(config_class=Config, initialize_db=True):
    """
    Flask application factory function.
    Creates and configures a Flask application instance.
    
    Args:
        config_class: Configuration class to use
        initialize_db: Whether to initialize the database (default: True)
    """
    # Create Flask application instance
    app = Flask(__name__, 
                template_folder='views/templates', 
                static_folder='views/static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Register routes and controllers
    register_routes(app)
    
    # Initialize database if requested
    if initialize_db:
        initialize_database()
    
    return app


def register_routes(app):
    """
    Register all application routes with their respective controllers.
    """
    try:
        from app.controllers.auth_controller import AuthController
        from app.controllers.admin_controller import AdminController
        from app.controllers.librarian_controller import LibrarianController
    except ImportError as e:
        print(f"Warning: Controller import failed: {e}")
        raise
    
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return AuthController.login()

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return AuthController.signup()

    @app.route('/logout')
    def logout():
        return AuthController.logout()

    @app.route('/dashboard')
    def dashboard():
        return AuthController.dashboard()

    @app.route('/admin/dashboard')
    def admin_dashboard():
        return AuthController.admin_dashboard()

    @app.route('/admin/member-management')
    def admin_member_management():
        return AdminController.member_management()

    @app.route('/admin/add-member', methods=['GET', 'POST'])
    def admin_add_member():
        return AdminController.add_member()

    @app.route('/admin/view-all-members')
    def admin_view_all_members():
        return AdminController.view_all_members()

    @app.route('/admin/edit-member', methods=['GET', 'POST'])
    def admin_edit_member():
        return AdminController.edit_member()

    @app.route('/admin/edit-member/<user_id>', methods=['GET', 'POST'])
    def admin_edit_member_by_id(user_id):
        return AdminController.edit_member_by_id(user_id)

    @app.route('/admin/delete-member', methods=['GET', 'POST'])
    def admin_delete_member():
        return AdminController.delete_member()

    @app.route('/admin/delete-member/<user_id>')
    def admin_delete_member_by_id(user_id):
        return AdminController.delete_member_by_id(user_id)

    @app.route('/librarian/dashboard')
    def librarian_dashboard():
        return LibrarianController.librarian_dashboard()

    @app.route('/librarian/book-issue', methods=['GET', 'POST'])
    def librarian_book_issue():
        return LibrarianController.book_issue()

    @app.route('/librarian/book-return', methods=['GET', 'POST'])
    def librarian_book_return():
        return LibrarianController.book_return()


def initialize_database():
    """
    Initialize database tables and sample data.
    """
    try:
        from app.utils.db_initializer import DatabaseInitializer
        DatabaseInitializer.initialize_all()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        # Don't fail the app creation if database init fails


# Create a global app instance for backward compatibility
# This allows existing code to use "from app import app"
# Database initialization is disabled here to avoid duplicate initialization
app = create_app(initialize_db=False)
