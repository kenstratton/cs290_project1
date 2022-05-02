from flask import render_template, url_for, redirect, flash, session, request, Response
from main import app, db
from main.models import User
from main.form import UserForm, UserLoginForm


# Check the login status of a user
def user_is_in():
    if 'user_name' in session:
        return True
    else:
        return False


# Top
@app.route('/')
def top():
    if not user_is_in():
        return redirect(url_for('entry'))

    return render_template(
        'app/app.html', type='top', title='LOG BASE', session=session)


# Add channel
@app.route('/add_channel')
def add_channel():
    if not user_is_in():
        return redirect(url_for('entry'))

    return render_template(
        'app/app.html', type='add_channel', title='Add Channel', session=session)


# Search channel
@app.route('/search')
def search():
    if not user_is_in():
        return redirect(url_for('entry'))

    return render_template(
        'app/app.html', type='search', title='Search', session=session)


# Settings
@app.route('/config')
def config():
    if not user_is_in():
        return redirect(url_for('entry'))

    return render_template(
        'app/app.html', type='config', title='Settings', session=session)


# Profile
@app.route('/profile')
def profile():
    if not user_is_in():
        return redirect(url_for('entry'))

    user = User.query.filter_by(name=session['user_name']).first()

    form = UserForm()
    form.name.data = user.name
    form.email.data = user.email

    return render_template(
        'app/app.html', type='profile', title='Profile', session=session, form=form)


# Entry for unauthenticated users
@app.route('/entry')
def entry():
    if user_is_in():
        return redirect(url_for('top'))
    else:
        return render_template(
            'app/app.html', type='entry', title='Entry', session=session)


# Log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if user_is_in():
        return redirect(url_for('top'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.verify_password(form.password.data):
            session['user_name'] = user.name
            return redirect(url_for('top'))

    return render_template(
        'app/app.html', type='login', title='Log In', session=session, form=form)


# Sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if user_is_in():
        return redirect(url_for('top'))

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(
                name = form.name.data,
                email = form.email.data,
                password = form.password.data)
            db.session.add(user)
            db.session.commit()
            session['user_name'] = user.name
            flash(f'Signed up successfully!')
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            return redirect(url_for('top'))
        else:
            flash(f'User <{user.name}> already exists!')

    return render_template(
        'app/app.html', type='signup', title='Sign Up', form=form, session=session)


# Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('entry'))



# Admin ------------------------------------------

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    users = User.query.order_by(User.date_added)
    return render_template(
        'admin/admin.html', type='top', title='Admin', users=users)


@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user(user=None):
    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f"<{user.name}> added successfully!")
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            return redirect(url_for('admin'))
        else:
            flash(f"User <{user.name}> alerady exists!")

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