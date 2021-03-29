from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length,InputRequired
class LoginForm(FlaskForm):
    '''
        字段名称大小写敏感，不能以下划线或validate开头
    '''
    username = StringField('User Name',validators=[DataRequired(),InputRequired('Please Input User Name!')])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128),InputRequired('Please Input Password!')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')