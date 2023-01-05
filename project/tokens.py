from flask import abort
from project import app
from time import time
import jwt


# Return a token for confirmation of signup
def signup_token(form, expiration=3600):
    return jwt.encode({'name'     : form.name.data,
                       'email'    : form.email.data,
                       'psw' : form.psw.data,
                       'exp'      : time() + expiration},
                       app.config['SECRET_KEY'],
                       algorithm='HS256')


# Return a token for authentication to the password reset page
def psw_reset_token(email, expiration=1800):
    return jwt.encode({'email' : email,
                       'exp'   : time() + expiration},
                       app.config['SECRET_KEY'],
                       algorithm='HS256')


# Return data of a decoded token after checking its validity
def decode_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if data['exp'] > time():
            return data
        else:
            abort(404)
    except:
        abort(403)