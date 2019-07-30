# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, EqualTo, ValidationError
# from models import User
from flask import url_for, redirect


class InfoForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    birthday = StringField('Birthday', validators=[DataRequired()])