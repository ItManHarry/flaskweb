from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length,InputRequired
'''
    设置错误消息语言
    方式一：通过基类事项（Flask-WTF版本 > 0.14.2）
    方式二：实例化form实例时传入meta参数进行设置(此方式即使继承了基类，属性设置优先)：
    例：form = LoginForm(meta={'locales':['zh','zh_TW']})
    另外还需要设置全局变量WTF_I18N_ENABLED为False
'''
class BaseForm(FlaskForm):
    class Meta:
        locales = ['zh']

class LoginForm(BaseForm):
    '''
        字段名称大小写敏感，不能以下划线或validate开头
    '''
    username = StringField('User Name',validators=[DataRequired(),InputRequired('Please Input User Name!')])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128),InputRequired('Please Input Password!')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')