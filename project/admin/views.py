# project > admin > views.py


from ctypes.wintypes import HKEY
from flask import flash, redirect, render_template, url_for, Blueprint, session
import functools
from project import db
from project.models.user import User
from project.form import user_form
from time import time


admin_bp = Blueprint('admin', __name__,)


# Functions for Handling Resources within This Module -------------------

# Clear admin session
def clear_admin_session():
    session.pop('admin', None)

# Set session for user entry
def set_admin_session():
    session['admin'] = True
    session['admin_lifetime'] = time() + 3600

# Check session status of admin
def is_admin_in_session():
    if 'admin' in session:
        return True
    return False

# Check the login status of a user
def check_admin_lifetime():
    if is_admin_in_session():
        if session['admin_lifetime'] > time():
            session['admin_lifetime'] = time() + 3600
        else:
            clear_admin_session()




# Things to be processed before any request -----------------------------

@admin_bp.before_request
def before_request():
    check_admin_lifetime()




# Auxiliary methods for routing ---------------------------

# Redirect to the entry page without logged in status
def login_required(view):
    @functools.wraps(view)
    def censored_view(*args, **kwargs):
        if not is_admin_in_session():
            return redirect(url_for('admin.login'))
        return view(*args, **kwargs)

    return censored_view


# Redirect to the top page with logged in status
def is_logged_in(view):
    @functools.wraps(view)
    def censored_view(*args, **kwargs):
        if is_admin_in_session():
            return redirect(url_for('admin.admin'))
        return view(*args, **kwargs)

    return censored_view




# Admin pages ---------------------------------------------

# Login page
@admin_bp.route('/admin/login', methods=['GET', 'POST'])
@is_logged_in
def login():
    form = user_form(['email', 'psw'])

    if form.validate_on_submit():
        admin = User.query.filter_by(email=form.email.data).first()
        if admin and admin.verify_password(form.psw.data):
            set_admin_session()
            return redirect(url_for('admin.admin'))
        form.email.data = ''

    return render_template(
        'admin/admin.html', type='login_form', title='Admin / Log In', form=form, login=False)


# Logout
@admin_bp.route('/admin/logout')
@login_required
def logout():
    clear_admin_session()
    return redirect(url_for('admin.admin'))


# Top page
@admin_bp.route('/admin')
@login_required
def admin():
    users = User.query.order_by(User.date_added)
    return render_template(
        'admin/admin.html', type='top', title='Admin', users=users, login=True)


# Add User
@admin_bp.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = user_form(['name', 'email', 'psw', 'psw_conf', 'rgtr'], True)

    if form.validate_on_submit():
        existing_user = User.query.filter_by(name=form.name.data).first()
        if existing_user is None:
            user_to_add = User(
                name=form.name.data,
                email=form.email.data,
                password=form.psw.data,
                confirmed=True)
            db.session.add(user_to_add)
            db.session.commit()
            flash(f"<{user_to_add.name}> added successfully!")
            form.name.data = ''
            form.email.data = ''
            form.psw.data = ''
        else:
            flash(f"User <{existing_user.name}> alerady exists!")

    return render_template(
        'admin/admin.html', type='add_user', title='Admin / Add User', form=form, login=True)


@admin_bp.route('/admin/delete_user/<int:id>')
@login_required
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        name = user_to_delete.name
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User <{name}> deleted successfully!")
    except:
        flash('Woops!! There was a problem deleting a user. Try again...')

    return redirect(url_for('admin.admin'))