from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Validation classes
class ValidateLength(Length):
    def __init__(self, min, max):
        super().__init__(
            min=min,
            max=max,
            message=f"*Must be {min} - {max} characters long.")

class ValidateRequired(DataRequired):
    def __init__(self, type):
        super().__init__(
            message=f"*{type} is required.")

class ValidateEmail(Email):
    def __init__(self):
        super().__init__(
            message="*Invalid address (e.g 123@example.com).")

class ValidateEqual(EqualTo):
    def __init__(self, target):
        super().__init__(
            fieldname=target,
            message=f"*Must match the {target} field.")


# Form classes
class UserForm(FlaskForm):
    name = StringField("Nickname",[
        ValidateRequired('Nickname'),
        ValidateLength(3, 100)])

    email = EmailField("Email",[
        ValidateRequired('Email'),
        ValidateLength(3, 120),
        ValidateEmail()])

    password = PasswordField("Password",[
        ValidateRequired('Password'),
        ValidateLength(8, 100),
        ValidateEqual('confirm')])

    confirm  = PasswordField("Confirm Password")

    submit = SubmitField('Submit')

    def is_valid(self, target):
        result = 0
        if  (target =='name' and self.name.errors) or \
            (target =='email' and self.email.errors) or \
            (target =='password' and self.password.errors):
                result = 1
        return result
