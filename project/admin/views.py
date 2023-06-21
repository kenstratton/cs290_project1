# project > admin > views.py


from ctypes.wintypes import HKEY
from flask import Blueprint, g, session, request, flash, redirect, render_template, url_for
import functools
from project import db
from project.models.user import User
from project.form import user_form
from time import time


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Functions for Handling Resources within This Module -------------------

# Clear admin session
def clear_admin_session():
    session.pop('admin_id', None)
    g.admin = None


# Set session for user entry
def set_admin_session(admin, limit=3600):
    session['admin_id'] = admin.id
    session['admin_lifetime'] = time() + limit


def extend_admin_lifetime(limit=3600):
    session['admin_lifetime'] = time() + limit


# Check session status of admin
def is_admin_in_session():
    if 'admin_id' in session:
        return True
    return False


# Check if admin lifetime is expired
def is_admin_expired():
    if session['admin_lifetime'] < time():
        return True
    return False


# Check the login status of a user
def check_admin_lifetime():
    if is_admin_in_session():
        if not is_admin_expired():
            extend_admin_lifetime()
            g.admin = User.query.filter_by(id=session['admin_id']).first()
        else:
            clear_admin_session()


# フォーム内のチェックボックスの状態に応じて、特定のフィールドがもつvalidatorsの中身を調整します
def adjust_validators(form):
    # ユーザーがAdminとして登録される場合、名前をNoneで統一し、名前のvalidationを無効化します
    if "admin" in form.__dict__.keys():
        if form.admin.data:
            form.name.data = None
            form.name.nullify_validators()
        else:
            form.name.activate_validators()

    # パスワード更新がない場合、パスワードのvalidationを無効化します
    elif "psw_disabled" in form.__dict__.keys():
        if form.psw_disabled.data:
            form.psw.nullify_validators()
        else:
            form.psw.activate_validators()

    return form




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
            return redirect(url_for('admin.index'))
        return view(*args, **kwargs)

    return censored_view


# Render a template with specifickeywords
def render_temp(path, title=None, form=None, **kwrgs):
    return render_template(
        path,
        title=title,
        form=form,
        g=g,
        request=request,
        **kwrgs
        )




# Admin pages ---------------------------------------------

#【Login】
@admin_bp.route('/login', methods=['GET', 'POST'])
@is_logged_in
def login():
    form = user_form(['email', 'psw'], lgin_type="admin")

    if form.validate_on_submit():
        admin = User.query.filter_by(email=form.email.data, admin=True).first()
        if admin and admin.verify_password(form.psw.data):
            set_admin_session(admin)
            return redirect(url_for('admin.index'))

    return render_temp('project/admin/main/auth.html', 'Log In', form)


#【Logout】
@admin_bp.route('/logout')
@login_required
def logout():
    clear_admin_session()
    return redirect(url_for('admin.login'))


#【Top】
@admin_bp.route('/')
@login_required
def index():
    return render_temp('project/admin/main/index.html')


#【User Management】User List
@admin_bp.route('/user_list')
@login_required
def user_list():
    users = User.query.order_by(User.date_added)
    return render_temp('project/admin/main/user_list.html', 'Add User', users=users)


#【User Management】Add user
@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = user_form(['name', 'email', 'psw', 'psw_conf', 'admin'], True)

    if request.method == 'POST': 
        # ユーザーがAdminとして登録される場合、名前をNoneで統一し、名前のvalidationを無効化します
        form = adjust_validators(form)

        if form.validate_on_submit():
            user_to_add = User(
                name=form.name.data if not form.admin.data else "Administrator",
                email=form.email.data,
                password=form.psw.data,
                admin=form.admin.data
            )
            db.session.add(user_to_add)
            db.session.commit()
            flash(f"User [ {user_to_add.name} ] was successfully added!")
            form.name.data = ''
            form.email.data = ''
            form.psw.data = ''

    return render_temp('project/admin/main/add_user.html', 'Add User', form)


#【User Management】Edit user
@admin_bp.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    form = user_form(['name', 'email', 'psw', 'psw_conf', 'psw_disabled', 'admin'], True, user.id)

    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.admin.data = user.admin

    elif request.method == 'POST': 
        # ユーザーがAdminとして登録される場合、名前をNoneで統一し、名前のvalidationを無効化します
        if form.admin.data:
            form.name.data = None
            form.name.nullify_validators()
        else:
            form.name.activate_validators()

        # パスワード更新がない場合、パスワードのvalidationを無効化します
        if form.psw_disabled.data:
            form.psw.nullify_validators()
        else:
            form.psw.activate_validators()

        if form.validate_on_submit():
            if not form.psw_disabled.data : user.password = form.psw.data
            user.name = form.name.data
            user.email = form.email.data
            user.admin = form.admin.data
            db.session.commit()
            flash(f"User [ id:{user.id} ] was successfully updated!")
            return redirect(url_for('admin.edit_user', id=int(user.id)))

    return render_temp('project/admin/main/manage_user.html', 'Edit User', form, user_id=id)


#【User Management】Delete user
@admin_bp.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        name = user_to_delete.name
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User [ {name} ] was successfully deleted!")
    except:
        flash('Woops!! There was a problem deleting a user. Try again...')

    return redirect(url_for('admin.user_list'))




# やること
# ユーザーフィルターしよう！(登録順, adminのみ, 一般のみ, )
# ユーザー検索(email, name) 非同期？ いやいい
#* ページネーションつけよう! (user_list)