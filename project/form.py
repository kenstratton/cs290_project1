from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from project.models.user import User




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


# Data uniqueness
class ValidateUnique(object):
    def __init__(self, type, class_member):
        self.message = f"*The {type} has been alerady registered."
        self.class_member = class_member

    def __call__(self, form, field):
        existing_user = User.query.filter(self.class_member==field.data).first()

        if existing_user:
            raise ValidationError(self.message)


# Non validation class
class Pass(object):
    def __call__(self, *args, **kwds):
        pass




# Form classes --------------------------------------------

# Base
class Form(FlaskForm):
    submit = SubmitField('Submit')

    def is_valid(self, type):
        result = 0
        if  (self[type].errors):
                result = 1
        return result


def user_form(prop=None, rgtr=False):
    class StaticForm(Form):
        pass
    
    if 'name' in prop:
        validate_unique = ValidateUnique('nickname', User.name) if rgtr else Pass()
        StaticForm.name = StringField('Nickname', [
            ValidateRequired('Nickname'),
            ValidateLength(3, 100),
            validate_unique])

    if 'email' in prop:
        validate_unique = ValidateUnique('email', User.email) if rgtr else Pass()
        StaticForm.email = EmailField('Email', [
            ValidateRequired('Email'),
            ValidateLength(3, 120),
            ValidateEmail(),
            validate_unique])

    if 'email_auth' in prop:
        StaticForm.email = EmailField('Email', [
            ValidateRequired('Email'),
            ValidateLength(3, 120),
            ValidateEmail()])

    if 'pl_info' in prop:
        StaticForm.pl_info = StringField('Nickname / Email', [
            ValidateRequired('Nickname / Email'),
            ValidateLength(3, 100)])

    if 'psw' in prop:
        StaticForm.psw = PasswordField('Password', [
            ValidateRequired('Password'),
            ValidateLength(8, 100)])

    if 'psw_conf' in prop:
        StaticForm.psw = PasswordField('Password', [
            ValidateRequired('Password'),
            ValidateLength(8, 100),
            ValidateEqual('conf')])

        StaticForm.conf  = PasswordField('Confirm Password')

    return StaticForm()