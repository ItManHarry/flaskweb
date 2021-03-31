from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,MultipleFileField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired, Length,InputRequired
from wtforms.validators import ValidationError
from flask_ckeditor import CKEditorField
'''
    全局验证器
'''
def validate_adminpwd(form, field):
    if field.data != '12345678':
        raise ValidationError('管理员密码错误!')
'''
    全局验证器，自定义错误消息
'''
def is_admin(message=None):
    if message is None:
        message = '请输入管理员账号'
    def _is_admin(form, field):
        if field.data != 'admin':
            raise ValidationError(message)
    return _is_admin
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
'''
    登录表单
'''
class LoginForm(BaseForm):
    '''
        字段名称大小写敏感，不能以下划线或validate开头
        注：即使用全局校验器又使用了行内校验器的情况，两个校验器均生效
    '''
    username = StringField('User Name',validators=[DataRequired(),InputRequired('Please Input User Name!'),is_admin('账号为非管理员账号,请更正!')])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128),InputRequired('Please Input Password!'),validate_adminpwd])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    '''
        自定义验证器 - 行内验证器
        
    '''
    def validate_username(self, field):
        if field.data != 'admin':
            raise ValidationError('请输入管理员账号!')
'''
    单个文件上传表单
'''
class SingleFileForm(BaseForm):
    photo = FileField('Upload Image',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField('Upload')
class MultipleFileForm(BaseForm):
    photos = MultipleFileField('Upload Images',validators=[DataRequired()])
    submit = SubmitField('Upload')
class RichEditorForm(BaseForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')