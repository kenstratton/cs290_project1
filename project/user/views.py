# project > user > views.py


from tabnanny import check
from flask import Blueprint, g, request, session, flash, redirect, render_template, url_for
from sqlalchemy import or_
from functools import wraps
from project import db # , assets
from project.models.user import User
from project.form import user_form
from time import time
from project.email import send_email
from project.tokens import signup_token, psw_reset_token, decode_token


user_bp = Blueprint('user', __name__,)


# Functions for Handling Resources within This Module -------------------

# Seach user from name or email
def search_user(name=None, email=None):
    user = User.query.filter(
        or_(
            User.name==name,
            User.email==email
        )).first()
    return user


# Clear user-related session status
def clear_user_session():
    session.pop('user_id', None)
    session.pop('auth', None)


# Set session for logged-in user
def set_user_session(user, limit=3600):
    clear_user_session()  # -> to reset session['auth'] generated before login
    session['user_id'] = user.id
    session['user_lifetime'] = time() + limit


# Set session for authenticated user
def set_auth_session(limit=1800):
    session['auth'] = True
    session['auth_lifetime'] = time() + limit


# Check if user is logged in
def is_user_in_session():
    if 'user_id' in session:
        return True
    return False


# Check if user is authenticated for particular pages
def is_auth_in_session():
    if 'auth' in session:
        return True
    return False


# Check if user lifetime is expired
def is_user_expired():
    if session['user_lifetime'] < time():
        return True
    return False


# Check if authentication lifetime is expired
def is_auth_expired():
    if session['auth_lifetime'] < time():
        return True
    return False


# If user lifetime and manage user-related session status
def check_user_lifetime():
    if is_user_in_session():
        if not is_user_expired():
            session['user_lifetime'] = time() + 3600
            g.user = User.query.filter_by(id=session['user_id']).first()
        else:
            clear_user_session()
            g.user = None


# Check auth lifetime and manage session status only of auth
def check_auth_lifetime():
    if is_auth_in_session():
        if is_auth_expired():
            session.pop('auth', None)


# Render a template with specific keywords
def render_temp(path, title=None, form=None, **kwrgs):
    return render_template(
        path,
        title=title,
        form=form,
        session=session,
        # assets=assets,
        **kwrgs
        )




# Things to be processed before any request -----------------------------

@user_bp.before_request
def before_request():
    check_user_lifetime()
    check_auth_lifetime()




# Functions for Supporting Routing --------------------------------------
# To the top page if a user is logged in 
def is_logged_in(view):
    @wraps(view)
    def censored_view(*args, **kwargs):
        if is_user_in_session():
            return redirect(url_for('user.index'))
        return view(*args, **kwargs)
    return censored_view


# To the initial page if a user is NOT logged in
def login_required(view):
    @wraps(view)
    def censored_view(*args, **kwargs):
        if not is_user_in_session():
            return redirect(url_for('user.intl'))
        return view(*args, **kwargs)
    return censored_view


# To the email authentication page if user is NOT authenticated
def authentication_required(type, dest=None):
    def authentication_required(view):
        @wraps(view)
        def censored_view(*args, **kwargs):
            if is_auth_in_session():
                return view(*args, **kwargs)
            elif type=='reset_psw':
                return redirect(url_for('user.forgot_password'))
            elif type=='update_info':
                return redirect(url_for('user.password_auth', dest=dest))
        return censored_view
    return authentication_required




# Views for Incidents ---------------------------------------------------

# Maintenance page
@user_bp.route('/maintenance')
def under_maintenace():
    return render_temp('management/maintenance.html')




# Views for unauthorized users  -----------------------------------------

# Initial page for unauthorized users
@user_bp.route('/intl')
@is_logged_in
def intl():
    return render_temp('project/user/main/intl.html')


#【Sign up】Sign up
@user_bp.route('/signup', methods=['GET', 'POST'])
@is_logged_in
def signup():
    form = user_form(['name', 'email', 'psw_conf'], True)

    if form.validate_on_submit():
        subject = "【Log Base】Please confirm your email !"
        token = signup_token(form)
        url = url_for('user.confirm_signup', token=token, _external=True)
        html = render_temp('project/user/email/confirm_user_account.html', url=url)
        send_email(form.email.data, subject, html)
        flash(f"We sent a user authentication email to [ {form.email.data} ]. Activate your account via the email.")
        return redirect(url_for('user.intl'))

    return render_temp('project/user/main/auth.html', 'Sign Up', form)


#【Sign up】Confirm a request to create user account
@user_bp.route('/signup_conf/<token>')
@is_logged_in
def confirm_signup(token):
    data = decode_token(token)

    user_to_add = User(
        name = data['name'],
        email = data['email'],
        password = data['psw'])
    db.session.add(user_to_add)
    db.session.commit()
    set_user_session(user_to_add)
    flash('Your account was successfully activated! Now you have access to all LogBase features.')
    return redirect(url_for('user.index'))


#【Log In】
@user_bp.route('/login', methods=['GET', 'POST'])
@is_logged_in
def login():
    form = user_form(['pl_info', 'psw'])  #! pl て分かりにくない？

    if form.validate_on_submit(): #! search_user() name, email統一できる？
        user_to_login = search_user(form.pl_info.data, form.pl_info.data)

        if user_to_login and user_to_login.verify_password(form.psw.data):
            set_user_session(user_to_login)
            return redirect(url_for('user.index'))
        return redirect(url_for('user.login'))

    return render_temp('project/user/main/auth.html', 'Log In', form)


#【Log out】
@user_bp.route('/logout')
@login_required
def logout():
    clear_user_session()
    return redirect(url_for('user.intl'))




# Views for BOTH authorized and unauthorized users  ---------------------

#【Password Reset】
@user_bp.route('/forgot_password', methods=['GET', 'POST'])
@is_logged_in
def forgot_password():
    form = user_form(['email_auth'])

    if form.validate_on_submit():
        email = form.email.data
        user = search_user(email=email)

        if user == None:
            flash(f'User of {email} doesn\'t exist.')
            return redirect(url_for('user.forgot_password'))

        subject = "【Log Base】Please confirm your email !"
        token = psw_reset_token(email)
        url = url_for('user.confirm_password_reset', token=token, _external=True)
        html = render_temp('project/user/email/confirm_password_reset.html', url=url)
        send_email(email, subject, html)
        flash(f"We sent a confirmation email to [ {email} ]. Confirm the email to reset the password for your account.")
        return redirect(url_for('user.intl'))

    return render_temp(
        'project/user/main/auth.html',
        'Forgot Password?', form)


#【Password Reset】Inspect a received token and go to the reset page 
@user_bp.route('/confirm_password_reset/<token>')
@is_logged_in
def confirm_password_reset(token):
    data = decode_token(token)
    return redirect(url_for(
        'user.reset_password', email=data['email']))


#! tokenの時間制限。。。役割果たしてる？
#! パスワへんこうできんくね？
#*【Password Reset】Form page to reset password 
@user_bp.route('/reset_password/<email>', methods=['GET', 'POST'])
@is_logged_in
def reset_password(email):
    form = user_form(['psw_conf'])

    set_auth_session()
    if form.validate_on_submit():
        user = search_user(email=email)
        if user:
            user.password = form.psw.data
            user.name = "ken"
            db.session.commit()
            # flash('Your new password was successfully set!')
            psw = user.verify_password(form.psw.data)
            flash(f'{psw}')
            return redirect(url_for('user.intl'))

    return render_temp(
        'project/user/main/auth.html',
        'Reset Passoword', form)




# Views for authorized users -------------------------------------------

#* Top
@user_bp.route('/')
@login_required
def index():
    return render_temp('project/user/main/index.html', 'LOG BASE')


#* Add channel
@user_bp.route('/add_channel')
@login_required
def add_channel():
    return render_temp('user/contents/main/add_channel.html', 'Add Channel')


#* Search channel
@user_bp.route('/search')
@login_required
def search():
    return render_temp('user/laycout/main/search.html', 'Search')



#* Settings
@user_bp.route('/config')
@login_required
def config():
    return render_temp('user/contents/setting/config.html', 'Settings')


#* Profile
@user_bp.route('/profile')
@login_required
def profile():
    return render_temp('user/contents/profile/profile.html', 'Profile', user=g.user)


#* Password Authentication
@user_bp.route('/profile/<dest>/auth', methods=['GET', 'POST'])
@login_required
def password_auth(dest):
    form = user_form(['psw'])

    if request.method == 'POST':
        user_to_verify = User.query.filter_by(id=session['user_id']).first()
        if form.validate_on_submit \
        and user_to_verify.verify_password(form.psw.data):
            set_auth_session()
            flash('Successfully authenticated!')
            return redirect(url_for(dest))

    return render_temp('user/contents/auth/request_profile_update.html', 'Profile / Authentication', form)


#* Update Name & Email
@user_bp.route('/profile/basic_info', methods=['GET', 'POST'])
@login_required
@authentication_required('update_info', 'user.basic_info')
def basic_info():
    form = user_form(['name', 'email'], True)

    if request.method == 'GET':
        form.name.data = g.user.name
        form.email.data = g.user.email

    elif form.validate_on_submit():
        user_to_update = User.query.filter_by(id=g.user.id).first()
        user_to_update.name = form.name.data
        user_to_update.email = form.email.data
        db.session.commit()
        flash('Your basic info was changed.')

    return render_temp('user/contents/profile/update_basic_info.html', 'Profile / Basic Info', form)


#* Alter Password
@user_bp.route('/profile/password', methods=['GET', 'POST'])
@login_required
@authentication_required('update_info', 'user.password')
def password():
    form = user_form(['psw_conf'])

    if form.validate_on_submit():
        g.user.password = form.psw.data
        db.session.commit()
        flash('Your password was changed.')
        form.psw.data = ''

    return render_temp('user/contents/profile/reset_password.html', 'Profile / Password', form)
