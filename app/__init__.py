from flask import Flask
from config import Config
from flask import Flask
from app.controllers.auth_controller import AuthController
from app.models.user import User

def create_app():
    app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
    app.secret_key = 'replace_this_with_a_secure_random_key_2025'

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

    @app.route('/admin/dashboard')
    def admin_dashboard():
        return AuthController.admin_dashboard()

    @app.route('/admin/book-status')
    def admin_book_status():
        return AuthController.admin_book_status()

    @app.route('/librarian/dashboard')
    def librarian_dashboard():
        return AuthController.librarian_dashboard()

    @app.route('/librarian/book-status')
    def librarian_book_status():
        return AuthController.librarian_book_status()

    @app.route('/student/dashboard')
    def student_dashboard():
        return AuthController.student_dashboard()

    @app.route('/student/book-status')
    def student_book_status():
        return AuthController.student_book_status()

    return app
