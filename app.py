from flask import Flask
from config import Config
from app.controllers.auth_controller import AuthController
from app.controllers.admin_controller import AdminController
from app.controllers.librarian_controller import LibrarianController
from app.controllers.student_controller import StudentController
from app.utils.db_initializer import DatabaseInitializer

app = Flask(__name__, template_folder='app/views/templates', static_folder='app/views/static')
app.config.from_object(Config)

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

@app.route('/admin/book-management', methods=['GET', 'POST'])
def admin_book_management():
    return AdminController.book_management()

@app.route('/admin/book-status')
def admin_book_status():
    return AdminController.book_status()

@app.route('/admin/fines-detail')
def admin_fines_detail():
    return AdminController.fines_detail()

@app.route('/librarian/dashboard')
def librarian_dashboard():
    return LibrarianController.librarian_dashboard()

@app.route('/librarian/book-management', methods=['GET', 'POST'])
def librarian_book_management():
    return LibrarianController.book_management()

@app.route('/librarian/book-issue', methods=['GET', 'POST'])
def librarian_book_issue():
    return LibrarianController.book_issue()

@app.route('/librarian/book-return', methods=['GET', 'POST'])
def librarian_book_return():
    return LibrarianController.book_return()

@app.route('/librarian/transaction-history')
def librarian_transaction_history():
    return LibrarianController.transaction_history()

@app.route('/librarian/book-issue-return')
def librarian_book_issue_return():
    return LibrarianController.book_issue_return()

@app.route('/librarian/notification-system')
def librarian_notification_system():
    return LibrarianController.notification_system()

@app.route('/librarian/book-status')
def librarian_book_status():
    return LibrarianController.book_status()

@app.route('/librarian/fines-management')
def librarian_fines_management():
    return LibrarianController.fines_management()

@app.route('/librarian/book-reservation', methods=['GET', 'POST'])
def librarian_book_reservation():
    return LibrarianController.book_reservation()

@app.route('/student/dashboard')
def student_dashboard():
    return StudentController.student_dashboard()

@app.route('/student/book-status')
def student_book_status():
    return StudentController.book_status()

@app.route('/student/book-reservation', methods=['GET', 'POST'])
def student_book_reservation():
    return StudentController.book_reservation()

@app.route('/student/account-status')
def student_account_status():
    return StudentController.account_status()

@app.route('/student/your-books')
def student_your_books():
    return StudentController.your_books()

if __name__ == '__main__':
    DatabaseInitializer.initialize_all()
    app.run(debug=True)
