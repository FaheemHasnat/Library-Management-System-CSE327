from flask import render_template, session, redirect, url_for, flash


class AdminController:
    @staticmethod
    def check_admin_access():
        if 'user_id' not in session or session.get('user_role') != 'Admin':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return None
