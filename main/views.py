from crypt import methods
import functools
from flask import g, flash, redirect, render_template, request, url_for, session
from sqlalchemy import or_ 
from main import app, db
from main.models import User
from main.form import UserForm, UserLoginForm, PasswordAuthForm, UserUpdateForm, PasswordUpdateForm




# In-module methods ---------------------------------------

# Check the login status of a user
def user_is_in():
    if 'user_id' in session:
        return True
    return False

def is_authentificated():
    if 'authentificated' in session:
        return True
    return False




# Auxiliary methods for routing ---------------------------

# Get data of a user to be logged in
@app.before_request
def load_logged_in_user():
    if user_is_in():
        g.user = User.query.filter_by(id=session['user_id']).first()
    else:
        g.user = None


# Redirect to the entry page without logged in status
def login_required(view):
    @functools.wraps(view)
    def censored_view(*args, **kwargs):
        if not user_is_in():
            return redirect(url_for('entry'))
        return view(*args, **kwargs)

    return censored_view


# Redirect to the top page with logged in status
def is_logged_in(view):
    @functools.wraps(view)
    def censored_view(*args, **kwargs):
        if user_is_in():
            return redirect(url_for('top'))
        return view(*args, **kwargs)

    return censored_view


def authentification_required(dest):
    def authentification_required(view):
        @functools.wraps(view)
        def censored_view(*args, **kwargs):
            if not is_authentificated():
                return redirect(url_for('password_auth', dest=dest))
            return view(*args, **kwargs)

        return censored_view
    return authentification_required



# Custom error pages --------------------------------------

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html'), 500




# Maintenance page ----------------------------------------

# Invalid URL
@app.route('/maintenance')
def under_maintenace():
    return render_template('management/maintenance.html')




# Application ---------------------------------------------

# Entry for unauthenticated users
@app.route('/entry')
@is_logged_in
def entry():
    return render_template(
        'app/app.html', type='entry', title='Entry', session=session)


# Sign up
@app.route('/signup', methods=['GET', 'POST'])
@is_logged_in
def signup():
    form = UserForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(name=form.name.data).first()
        if existing_user is None:
            user_to_add = User(
                name = form.name.data,
                email = form.email.data,
                password = form.password.data)
            db.session.add(user_to_add)
            db.session.commit()
            session['user_id'] = user_to_add.id
            flash(f'Signed up successfully!')
            return redirect(url_for('top'))
        else:
            flash(f'User <{existing_user.name}> already exists!')

    return render_template(
        'app/app.html', type='signup', title='Sign Up', form=form, session=session)


# Log in
@app.route('/login', methods=['GET', 'POST'])
@is_logged_in
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        user_to_login = User.query.filter(
            or_(
                User.name==form.name_or_email.data,
                User.email==form.name_or_email.data
            )).first()
        if user_to_login and user_to_login.verify_password(form.password.data):
            session['user_id'] = user_to_login.id
            return redirect(url_for('top'))

    return render_template(
        'app/app.html', type='login', title='Log In', session=session, form=form)


# Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('entry'))


# Top
@app.route('/')
@login_required
def top():
    return render_template(
        'app/app.html', type='top', title='LOG BASE', session=session)


# Add channel
@app.route('/add_channel')
@login_required
def add_channel():
    return render_template(
        'app/app.html', type='add_channel', title='Add Channel', session=session)


# Search channel
@app.route('/search')
@login_required
def search():
    return render_template(
        'app/app.html', type='search', title='Search', session=session)


# Settings
@app.route('/config')
@login_required
def config():
    return render_template(
        'app/app.html', type='config', title='Settings', session=session)


# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template(
        'app/app.html', type='profile', title='Profile', session=session, user=g.user)


# Password Authentification
@app.route('/profile/<string:dest>/auth', methods=['GET', 'POST'])
@login_required
def password_auth(dest):
    form = PasswordAuthForm()

    if request.method == 'POST':
        user_to_verify = User.query.filter_by(id=session['user_id']).first()
        if form.validate_on_submit \
        and user_to_verify.verify_password(form.password.data):
            session['authentificated'] = True
            flash('Successfully authentificated!')
            return redirect(url_for(dest))

    return render_template(
        'app/app.html',
        type='profile/auth',
        title='Profile / Authentification',
        session=session, form=form)


# Update Name & Email
@app.route('/profile/basic_info', methods=['GET', 'POST'])
@login_required
@authentification_required('basic_info')
def basic_info():
    form = UserUpdateForm()

    if request.method == 'GET':
        form.name.data = g.user.name
        form.email.data = g.user.email

    elif form.validate_on_submit():
        user_to_update = User.query.filter_by(id=g.user.id).first()
        user_to_update.name = form.name.data
        user_to_update.email = form.email.data
        db.session.commit()
        flash('Your basic info was changed.')

    return render_template(
        'app/app.html',
        type='profile/basic_info',
        title='Profile / Basic Info',
        session=session, form=form)


# Update Password
@app.route('/profile/password', methods=['GET', 'POST'])
@login_required
@authentification_required('password')
def password():
    form = PasswordUpdateForm()

    if form.validate_on_submit():
        user_to_update = User.query.filter_by(id=g.user.id).first()
        user_to_update.password = form.password.data
        db.session.commit()
        flash('Your password was changed.')
        form.password.data = ''

    return render_template(
        'app/app.html',
        type='profile/password',
        title='Profile / Password',
        session=session, form=form)




# Admin ---------------------------------------------------

# Top page
@app.route('/admin')
def admin():
    users = User.query.order_by(User.date_added)
    return render_template(
        'admin/admin.html', type='top', title='Admin', users=users)


# Add User
@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user(user=None):
    form = UserForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(name=form.name.data).first()
        if existing_user is None:
            user_to_add = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data)
            db.session.add(user_to_add)
            db.session.commit()
            flash(f"<{user_to_add.name}> added successfully!")
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
        else:
            flash(f"User <{existing_user.name}> alerady exists!")

    return render_template(
        'admin/admin.html', type='add_user', title='Admin / Add User', form=form)


@app.route('/admin/delete_user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        name = user_to_delete.name
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User <{name}> deleted successfully!")
        return redirect(url_for('admin'))
    except:
        flash('Woops!! There was a problem deleting a user. Try again...')
        return redirect(url_for('admin'))