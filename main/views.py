from flask import render_template, url_for, redirect, flash, session, request, Response
from main import app, db
from main.models import User
from main.form import UserForm

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    users = User.query.order_by(User.date_added)
    return render_template('admin.html', type='admin', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user(user=None):
    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.name.data).first()
        if user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f"<{form.name.data}> added successfully!")
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            return redirect(url_for('admin'))
        else:
            flash(f"<{user.name}> alerady exists!")

    return render_template('add_user.html', type='admin', form=form)


# Top
@app.route('/')
def top():
    return render_template('top.html', type='in')

# Add channel
@app.route('/add_channel')
def add_channel():
    return render_template('add_channel.html', type='in')

# Search channel
@app.route('/search')
def search():
    return render_template('search.html', type='in')

# Settings
@app.route('/config')
def config():
    return render_template('config.html', type='in')

# Profile
@app.route('/profile')
def profile():
    return render_template('profile.html', type='in')

# Entry for unauthenticated users
@app.route('/entry')
def entry():
    return render_template('entry.html', type='out')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', type='out')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', type='out')

    # Deals with User's request to sign up
    if request.method == 'POST':
        user_name = request.form['user_name']
        if not user_name:
            return render_template('signup.html', type='out')
        user = User.query.filter_by(name=user_name).first()
        if user:
            return render_template('top.html', type='in')
        else:
            password = request.form['password']
            if not password:
                return render_template('signup.html', type='out')
            hashed_password = sha256((user_name + password + key.SALT).encode('utf-8')).hexdigest()
            user = User(user_name, hashed_password)
            db.session.add(user)
            db.session.commit()
            session['user_name'] = user_name
            return redirect(url_for('top', status='sign'))
    # If signed in already, transfers to a top page
    if 'user_name' in session:
        return redirect(url_for('top'))
    # Output HTML form
    return render_template('sign.html', type='sign_up', title='Sign up', error='')

    
