# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class InfoForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    user_id = StringField('user_id', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_check = PasswordField('Password_check', validators=[DataRequired(), EqualTo("password")])


class RecordForm(FlaskForm):
    record = StringField('record', validators=[DataRequired()])


class GroupForm(FlaskForm):
    group_id = StringField('group_id', validators=[DataRequired()])


class DialogForm(FlaskForm):
    my_chat = StringField('my_chat', validators=[DataRequired()])


class JoinForm(FlaskForm):
    searching = StringField('searching', validators=[DataRequired()])


class CommentForm(FlaskForm):
    comment = StringField('comment', validators=[DataRequired()])