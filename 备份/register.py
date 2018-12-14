from wtforms import Form, BooleanField, TextField, PasswordField, validators,StringField,PasswordField,SubmitField,RadioField
from wtforms.validators import DataRequired,EqualTo,Length

class RegistrationForm(Form):
    username = StringField("请输入用户名", validators=[DataRequired()])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequiredRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])