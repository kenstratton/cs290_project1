from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo




# Validation classes---------------------------------------

# Length
class ValidateLength(Length):
    def __init__(self, min, max):
        super().__init__(
            min=min,
            max=max,
            message=f"*Must be {min} - {max} characters long.")


# Required
class ValidateRequired(DataRequired):
    def __init__(self, type):
        super().__init__(
            message=f"*{type} is required.")


# Email
class ValidateEmail(Email):
    def __init__(self):
        super().__init__(
            message="*Invalid address (e.g email@address.com).")


# Equality
class ValidateEqual(EqualTo):
    def __init__(self, type):
        super().__init__(
            fieldname=type,
            message=f"*Must match the {type} field.")




# Form classes --------------------------------------------

# Base
class Form(FlaskForm):
    submit = SubmitField('Submit')

    def is_valid(self, type):
        result = 0
        if  (self[type].errors):
                result = 1
        return result


# User form
class UserForm(Form):
    name = StringField('Nickname', [
        ValidateRequired('Nickname'),
        ValidateLength(3, 100)])

    email = EmailField('Email', [
        ValidateRequired('Email'),
        ValidateLength(3, 120),
        ValidateEmail()])

    password = PasswordField('Password', [
        ValidateRequired('Password'),
        ValidateLength(8, 100),
        ValidateEqual('confirm')])

    confirm  = PasswordField('Confirm Password')


# Login form
class UserLoginForm(Form):
    name_or_email = StringField('Nickname / Email', [
        ValidateRequired('Nickname / Email'),
        ValidateLength(3, 100)])

    password = PasswordField('Password', [
        ValidateRequired('Password'),
        ValidateLength(3, 100)])


# Password authentification form
class PasswordAuthForm(Form):
    password = PasswordField('Password', [
        ValidateRequired('Password'),
        ValidateLength(8, 100)])


# Update form (Name & Email)
class UserUpdateForm(Form):
    name = StringField('Nickname', [
        ValidateRequired('Nickname'),
        ValidateLength(3, 100)])

    email = EmailField('Email', [
        ValidateRequired('Email'),
        ValidateLength(3, 120),
        ValidateEmail()])


# Password update form
class PasswordUpdateForm(Form):
    password = PasswordField('Password', [
        ValidateRequired('Password'),
        ValidateLength(8, 100),
        ValidateEqual('confirm')])

    confirm  = PasswordField('Confirm Password')