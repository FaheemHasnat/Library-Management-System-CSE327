from flask import render_template, session, redirect, url_for, flash, request
from app.models.user import User
from app.models.book import Book
from app.utils.database import Database

class AdminController:
    @staticmethod
    def check_admin_access():
        if 'user_id' not in session or session.get('user_role') != 'Admin':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return None
    
    @staticmethod
    def member_management():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        total_members = AdminController.get_member_count()
        student_count = AdminController.get_member_count_by_role('Student')
        librarian_count = AdminController.get_member_count_by_role('Librarian')
        admin_count = AdminController.get_member_count_by_role('Admin')
        
        return render_template('admin/member_management.html', 
                             user_name=session.get('user_name'),
                             total_members=total_members,
                             student_count=student_count,
                             librarian_count=librarian_count,
                             admin_count=admin_count)
    
    @staticmethod
    def get_member_count():
        query = "SELECT COUNT(*) as count FROM users"
        result = Database.execute_single_query(query)
        return result['count'] if result else 0
    
    @staticmethod
    def get_member_count_by_role(role):
        query = "SELECT COUNT(*) as count FROM users WHERE Role = %s"
        result = Database.execute_single_query(query, (role,))
        return result['count'] if result else 0
    
    @staticmethod
    def add_member():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            role = request.form.get('role')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not all([name, email, role, password, confirm_password]):
                flash('Please fill in all fields', 'error')
                return render_template('admin/add_member.html', user_name=session.get('user_name'))
            
            if role not in ['Student', 'Librarian']:
                flash('Invalid role selected', 'error')
                return render_template('admin/add_member.html', user_name=session.get('user_name'))
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('admin/add_member.html', user_name=session.get('user_name'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return render_template('admin/add_member.html', user_name=session.get('user_name'))
            
            if User.get_by_email(email):
                flash('Email already exists', 'error')
                return render_template('admin/add_member.html', user_name=session.get('user_name'))
            
            user = User.create_user(name, email, password, role)
            
            if user:
                flash(f'Member {name} added successfully!', 'success')
                return redirect(url_for('admin_member_management'))
            else:
                flash('Error creating member. Please try again.', 'error')
        
        return render_template('admin/add_member.html', user_name=session.get('user_name'))
    
    @staticmethod
    def view_all_members():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        query = "SELECT UserID, Name, Email, Role FROM users ORDER BY Name"
        members = Database.execute_query(query)
        
        return render_template('admin/view_all_members.html', 
                             user_name=session.get('user_name'),
                             members=members or [])
    
    @staticmethod
    def edit_member():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        member = None
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'update':
                user_id = request.form.get('user_id')
                name = request.form.get('name')
                role = request.form.get('role')
                new_password = request.form.get('new_password')
                
                if not all([user_id, name, role]):
                    flash('Please fill in all required fields', 'error')
                    member = User.get_by_id(user_id)
                    return render_template('admin/edit_member.html', 
                                         user_name=session.get('user_name'),
                                         member=member)
                
                if role not in ['Student', 'Librarian', 'Admin']:
                    flash('Invalid role selected', 'error')
                    member = User.get_by_id(user_id)
                    return render_template('admin/edit_member.html', 
                                         user_name=session.get('user_name'),
                                         member=member)
                
                current_member = User.get_by_id(user_id)
                if AdminController.update_member(user_id, name, current_member.email, role, new_password):
                    flash('Member updated successfully!', 'success')
                    return redirect(url_for('admin_member_management'))
                else:
                    flash('Error updating member. Please try again.', 'error')
                    member = User.get_by_id(user_id)
            
            else:
                email = request.form.get('email')
                if email:
                    member = User.get_by_email(email)
                    if not member:
                        flash('Member not found with this email', 'error')
        
        return render_template('admin/edit_member.html', 
                             user_name=session.get('user_name'),
                             member=member)
    
    @staticmethod
    def edit_member_by_id(user_id):
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        member = User.get_by_id(user_id)
        
        if not member:
            flash('Member not found', 'error')
            return redirect(url_for('admin_member_management'))
        
        if request.method == 'POST':
            name = request.form.get('name')
            role = request.form.get('role')
            new_password = request.form.get('new_password')
            
            if not all([name, role]):
                flash('Please fill in all required fields', 'error')
                return render_template('admin/edit_member.html', 
                                     user_name=session.get('user_name'),
                                     member=member)
            
            if role not in ['Student', 'Librarian']:
                flash('Invalid role selected', 'error')
                return render_template('admin/edit_member.html', 
                                     user_name=session.get('user_name'),
                                     member=member)
            
            if AdminController.update_member(user_id, name, member.email, role, new_password):
                flash('Member updated successfully!', 'success')
                return redirect(url_for('admin_view_all_members'))
            else:
                flash('Error updating member. Please try again.', 'error')
        
        return render_template('admin/edit_member.html', 
                             user_name=session.get('user_name'),
                             member=member)
    
    @staticmethod
    def update_member(user_id, name, email, role, new_password=None):
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if new_password:
                    hashed_password = User.hash_password(new_password)
                    query = "UPDATE users SET Name = %s, Email = %s, Role = %s, Password = %s WHERE UserID = %s"
                    cursor.execute(query, (name, email, role, hashed_password, user_id))
                else:
                    query = "UPDATE users SET Name = %s, Email = %s, Role = %s WHERE UserID = %s"
                    cursor.execute(query, (name, email, role, user_id))
                
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating member: {e}")
                return False
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return False
    
    @staticmethod
    def delete_member():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        member = None
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'delete':
                user_id = request.form.get('user_id')
                
                if AdminController.delete_member_by_user_id(user_id):
                    flash('Member deleted successfully!', 'success')
                    return redirect(url_for('admin_member_management'))
                else:
                    flash('Error deleting member. Please try again.', 'error')
            
            else:
                email = request.form.get('email')
                if email:
                    member = User.get_by_email(email)
                    if not member:
                        flash('Member not found with this email', 'error')
        
        return render_template('admin/delete_member.html', 
                             user_name=session.get('user_name'),
                             member=member)
    
    @staticmethod
    def delete_member_by_id(user_id):
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        if AdminController.delete_member_by_user_id(user_id):
            flash('Member deleted successfully!', 'success')
        else:
            flash('Error deleting member. Please try again.', 'error')
        
        return redirect(url_for('admin_view_all_members'))
    
    @staticmethod
    def delete_member_by_user_id(user_id):
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "DELETE FROM users WHERE UserID = %s"
                cursor.execute(query, (user_id,))
                connection.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error deleting member: {e}")
                return False
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return False
    
    @staticmethod
    def book_management():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        subject_filter = request.args.get('subject', 'all')
        sort_by = request.args.get('sort', 'title')
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                title = request.form.get('title')
                author = request.form.get('author')
                subject = request.form.get('subject')
                isbn = request.form.get('isbn')
                
                if all([title, author, subject, isbn]):
                    if Book.add_book(title, author, subject, isbn):
                        flash('Book added successfully!', 'success')
                    else:
                        flash('Error adding book. Please try again.', 'error')
                else:
                    flash('Please fill in all fields', 'error')
                
                return redirect(url_for('admin_book_management'))
            
            elif action == 'delete':
                book_id = request.form.get('book_id')
                result = Book.delete_book(book_id)
                
                if result == True:
                    flash('Book deleted successfully!', 'success')
                elif result == "borrowed":
                    flash('Cannot delete book - it is currently borrowed', 'error')
                else:
                    flash('Error deleting book. Please try again.', 'error')
                
                return redirect(url_for('admin_book_management'))
            
            elif action == 'edit':
                book_id = request.form.get('book_id')
                title = request.form.get('title')
                author = request.form.get('author')
                subject = request.form.get('subject')
                isbn = request.form.get('isbn')
                
                if all([book_id, title, author, subject, isbn]):
                    if Book.update_book(book_id, title, author, subject, isbn):
                        flash('Book updated successfully!', 'success')
                    else:
                        flash('Error updating book. Please try again.', 'error')
                else:
                    flash('Please fill in all fields', 'error')
                
                return redirect(url_for('admin_book_management'))
        
        books = Book.get_all_books_with_filter(subject_filter, sort_by)
        subjects = Book.get_all_subjects()
        
        return render_template('admin/book_management.html', 
                             user_name=session.get('user_name'),
                             books=books,
                             subjects=subjects,
                             current_subject=subject_filter,
                             current_sort=sort_by)
    
    @staticmethod
    def book_status():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        books = Book.get_all_books()
        
        return render_template('admin/book_status.html', 
                             user_name=session.get('user_name'),
                             books=books)
    
    @staticmethod
    def fines_detail():
        access_check = AdminController.check_admin_access()
        if access_check:
            return access_check
        
        return render_template('admin/fines_detail.html', user_name=session.get('user_name'))
