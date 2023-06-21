from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, StopValidation, DataRequired, Length, Email, EqualTo
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
        super().__init__( message=f"*{type} is required." )


# Email
class ValidateEmail(Email):
    def __init__(self):
        super().__init__( message="*Invalid address (e.g email@address.com)." )


# Equality
class ValidateEqual(EqualTo):
    def __init__(self, type):
        super().__init__(
            fieldname=type,
            message=f"*Must match the {type} field.")


# Data uniqueness
class ValidateUnique(object):
    def __init__(self, type, class_member, user_id=None):
        self.message = f"*The {type} has alerady been registered."
        self.class_member = class_member
        self.user_id = user_id

    def __call__(self, form, field):
        existing_user = User.query.filter(self.class_member==field.data).first()

        if existing_user and (self.user_id == None or existing_user.id != self.user_id):
            raise ValidationError(self.message)


# Non existing user (unregistered or non-admin)
class ValidateNonExisting(object):
    def __init__(self, type, class_member, lgin_type=None):
        self.message = f"* User with this {type} doesn\'t exist."
        self.class_member = class_member
        self.lgin_type = lgin_type

    def __call__(self, form, field):
        user = User.query.filter(self.class_member==field.data).first()
        if user == None or (self.lgin_type == "user" and user.admin):
            raise ValidationError(self.message)


# Non validation class
class Pass(object):
    def __call__(self, *args, **kwds):
        pass




# Field classes --------------------------------------------

class MyStringField(StringField):
    def __init__(self, label, validators, **kwargs):
        super(MyStringField, self).__init__(label, validators, **kwargs)
        self.pre_validators = validators

    def nullify_validators(self):
        self.validators = [Pass()]

    def activate_validators(self):
        self.validators = self.pre_validators


class MyPasswordField(PasswordField):
    def __init__(self, label, validators, **kwargs):
        super(MyPasswordField, self).__init__(label, validators, **kwargs)
        self.pre_validators = validators

    def nullify_validators(self):
        self.validators = [Pass()]

    def activate_validators(self):
        self.validators = self.pre_validators




# Form classes --------------------------------------------

# Base
class Form(FlaskForm):
    submit = SubmitField('Submit')

    def is_valid(self, type):
        result = 0
        if  (self[type].errors):
                result = 1
        return result


def user_form(prop=None, rgstr=False, user_id=None, lgin_type=False): 
    class StaticForm(Form):
        pass
    
    if 'name' in prop:
        validate_unique = ValidateUnique('nickname', User.name, user_id) if rgstr else Pass()
        StaticForm.name = MyStringField('Nickname', [
            ValidateRequired('Nickname'),
            ValidateLength(3, 100),
            validate_unique])

    if 'email' in prop:
        validate_unique = ValidateUnique('email', User.email, user_id) if rgstr else Pass()
        validate_non_existing = ValidateNonExisting('email', User.email, lgin_type) if lgin_type else Pass()
        StaticForm.email = EmailField('Email', [
            ValidateRequired('Email'),
            ValidateLength(3, 120),
            ValidateEmail(),
            validate_unique,
            validate_non_existing])

    if 'psw' in prop:
        StaticForm.psw = PasswordField('Password', [
            ValidateRequired('Password'),
            ValidateLength(8, 100)])

    if 'psw_conf' in prop:
        StaticForm.psw = MyPasswordField('Password', [
            ValidateRequired('Password'),
            ValidateLength(8, 100),
            ValidateEqual('conf')])

        StaticForm.conf  = PasswordField('Confirm Password')

    # Adminのユーザー編集でパスワード以外を変更したい場合に使用します
    if 'psw_disabled' in prop:
        StaticForm.psw_disabled = BooleanField('No change of password')

    if 'admin' in prop:
        StaticForm.admin = BooleanField('Admin')

    return StaticForm()