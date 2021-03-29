from flask import Flask,request,make_response,jsonify,redirect,url_for,session,g,render_template,Markup,flash
from forms.forms import LoginForm
from urllib.parse import urlparse,urljoin
import json
import os
import time
app = Flask(__name__)
#如果要使用session，必须设置secret_key值
app.secret_key=os.getenv('SECRET_KEY', 'secretkey0001')
app.config['WTF_I18N_ENABLED'] = False
#自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
#钩子函数
@app.before_first_request
def init():
    print('Web App Start, Do The Init Action!!!')

@app.before_request
def reqintercepter():
    g.name = request.args.get('name', 'Harry')
    g.index = int(request.args.get('index', '1'))
    session['user'] = g.name
    print('Intercept every request!!!')

#自定义上下文
@app.context_processor
def inject_params():
    name = 'Jack'
    age = 25
    return dict(p_name=name,p_age=age)
#注册全局函数
@app.template_global()
def get_time():
    return 'Now is : %s, Time Zone is : %s' %(time.strftime('%Y年%m月%d日 %H时%M分%S秒'), time.tzname)

#自定义过滤器
@app.template_filter()
def musical(s):
    return s + ' - ' + Markup('&#9835;')

@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False
'''
    模板环境中的全局函数、过滤器和测试器分别存储在Enviroment 对象的globals 、filters 和
    tests 属性中，这三个属性都是字典对象。除了使用Flask 提供的装饰器和方法注册自定义函数，
    我们也可以直接操作这三个字典来添加相应的函数或变量，这通过向对应的字典属性中添加一
    个键值对实现，传人模板的名称作为键，对应的函数对象或变量作为值
'''
#添加全局函数&全局变量
def sayhello():
    return 'Hello, welcome you !!!'
globaltitle = 'Global Title'
app.jinja_env.globals['sayhello'] = sayhello
app.jinja_env.globals['globaltitle'] = globaltitle
#添加过滤器
def smiling(s):
    return s + '  :)'
app.jinja_env.filters['smiling'] = smiling
#添加测试器
def sam(n):
    if n == 'Sam':
        return True
    return False
app.jinja_env.tests['sam'] = sam
#删除Jinja2 语句后的第一个空行
app.jinja_env.trim_blocks=True
#删除Jinja2 语句所在行之前的空格和制表符(tabs)
app.jinja_env.lstrip_blocks=True
@app.route('/hello')
def hello():
    name = g.name
    if name  is None:
        name = request.cookies.get('python_cookie_name', name)
    print('Referrer : ', request.referrer,
          ', \nScheme : ', request.scheme,
          ', \nIs JSON : ', request.is_json,
          ', \nArguments : ', request.args,
          ',\nBlue Print : ', request.blueprint,
          ',\nCookies : ', request.cookies,
          ',\nData : ', request.data,
          ',\nEnd Point : ', request.endpoint,
          ',\nFiles : ', request.files,
          ',\nForm : ', request.form,
          ',\nValues : ', request.values,
          ',\nHeaders : ', request.headers)
    response = '<h1>Hello %s .</h1>' %name
    if 'logged_in' in session:
        response += '<h3>[Authenticated]</h3>'
    else:
        response += '<h3>[Not Authenticated]</h3>'
    return response

'''
    1. 绑定多个路由
    2. 动态路由
    3. 设置参数默认值
'''
@app.route('/greet',methods=['GET','POST'])
@app.route('/greet/<name>',methods=['GET','POST'])
def greet(name='Programmer'):
    print('Referrer : ', request.referrer,
          ', \nScheme : ', request.scheme,
          ', \nIs JSON : ', request.is_json,
          ', \nArguments : ', request.args,
          ',\nBlue Print : ', request.blueprint,
          ',\nCookies : ', request.cookies,
          ',\nData : ', request.data,
          ',\nEnd Point : ', request.endpoint,
          ',\nFiles : ', request.files,
          ',\nForm : ', request.form,
          ',\nValues : ', request.values,
          ',\nHeaders : ', request.headers)
    if request.args:
        for k,v in request.args.items():
            print('Key is : ', k, ', value is : ', v)
    else:
        print('Arguments is empty !!!')
    return '<h1>Hello , %s !</h1>' %name


@app.route('/any1/<any(blue,white,black,red,yellow):color>')
def any1(color):
    return '<p>My favourite color is : %s</p>' %color

colors = ['blue', 'yellow', 'black', 'red']
print('Colors are : ', str(colors)[1:-1])
print('Colors are : ', ','.join(colors))
#方式一
#@app.route('/any2/<any(%s):color>' %','.join(colors))
#方式二
@app.route('/any2/<any(%s):color>' %str(colors)[1:-1])
def any2(color):
    return '<p>My favourite color is : %s</p>' % color

'''
    相应格式
    1. 纯文本
    2. HTML(默认)
    3. XML
    4. JSON
'''

@app.route('/resp/plain')
def plain():
    response = make_response('<h1>Hello Harry, this is plain text!</h1>')
    response.mimetype = 'text/plain'
    return response

htmlstr = '''
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <hl >No te</ hl>
        <p>to : Peter</ p>
        <p>from : Jane</p>
        <p>heading : Rem 工n d er</ p >
        <p>body : <strong>Don ' t forget the party 1</strong></p>
    </body>
    </html>
'''
@app.route('/resp/html')
def html():
    response = make_response(htmlstr)
    return response

xmlstr = '''  
    <?xml version="1.0" encoding="UTF-8"?>
    <note>
        <to>Peter</to>
        <from>Jane</from>
        <heading>Reminder</heading>
        <body>Don’t forget the party </body>
    </note>
'''
@app.route('/resp/xml')
def xml():
    response = make_response(xmlstr)
    response.mimetype = 'application/xml'
    return response

jsonstr = '''
    {
        "note":{
            "to":"Peter",
            "from":"Jack",
            "heading":"Reminder",
            "body":"Don't forget the party!"
        }
    }
'''
@app.route('/resp/json')
def json1():
    response = make_response(jsonstr)
    response.mimetype = 'application/json'
    return response

'''
    1. 使用Python标准库中的json模块结合设置mime类型可将Python的字典、数组、元组序列化后返回json数据
    2. 使用Flask框架的jsonify()函数可以直接将Python数据返回json数据，而且不用设置mime类型,参数可以
       传入普通参数、关键字参数、或者字典、数组、元组
'''
data = {'name':'Jack','age':38,'email':'xxx@xxx.com'}
@app.route('/resp/json2')
def json2():
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response

@app.route('/resp/json3')
def json3():
    return jsonify(name='Tom',age=38,email='tom@163.com')

@app.route('/resp/json4')
def json4():
    return jsonify([1,2,3,4,5])

'''
    Response类属性方法
    1. headers：一个Werkzeug 的Headers 对象， 表示响应首部，可以像字典一样
    2. status：状态码，文本类型
    3. status_code：状态码，整型
    4. mimetype：MIME 类型（仅包括内容类型部分）
    5. set_cookie()：用来设置一个cookie，参数如下：
        5.1. key：键值
        5.2. value:cookie值
        5.3. max_age:有效时间，单位秒。默认是浏览器关闭即失效
        5.4. expires:具体的过期时间，一个datatime或者unix时间戳
        5.5. path:限定只在给定的路径内可用，默认整个域名
        5.6. domain:设置cookie可用的域名
        5.7. secure:如果设置True，只能通过https访问
        5.8. httponly:如果设置为True，客户端JavaScript获取cookie功能将被禁用        
'''
@app.route('/set/cookie/<name>')
def setcookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie(key='python_cookie_name', value=name)
    return response

'''
    session 指用户会话（ us巳r session ）， 又称为对话（ dialogue), 即
    服务器和客户揣/浏览器之间或桌面程序和用户之间建立的交互活动。
    在Flask 中， session 对象用来加密Cookie 。
    默认情况下，它会把数据存储在浏览器上一个名为session 的cookie 里
'''

@app.route('/login')
def login():
    print('App Secret Key Is : ', app.secret_key)
    session['logged_in'] = True
    session['logged_name'] = g.name
    return redirect(url_for('hello'))
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    session.pop('loginuser', None)
    return redirect(url_for('index'))

#重定向回到上一个页面
@app.route('/foo')
def foo():
    return '''
        <h1>Foo Page</h1>
        <a href = "%s">Get Back 1</a>&nbsp;&nbsp;
        <a href = "%s">Get Back 2</a>&nbsp;&nbsp;
        <a href = "%s">Get Back 3</a>&nbsp;&nbsp;
    ''' % (url_for('get_back1'), url_for('get_back2', next=request.full_path), url_for('get_back_for_all'))
@app.route('/bar')
def bar():
    return '''
           <h1>Bar Page</h1>
           <a href = "%s">Get Back 1</a>&nbsp;&nbsp;
           <a href = "%s">Get Back 2</a>&nbsp;&nbsp;
           <a href = "%s">Get Back 3</a>&nbsp;&nbsp;
    ''' % (url_for('get_back1'),url_for('get_back2', next=request.full_path), url_for('get_back_for_all',next='http://www.baidu.com'))
#URL地址安全验证 - 确认是否属于程序内部
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc
#实现方式一：使用请求对象的referrer属性获取上一个url地址
@app.route('/get_back1')
def get_back1():
    #do something
    return redirect(request.referrer or url_for('hello'))
#实现方式二：手动获取url，使用next参数进行传递
@app.route('/get_back2')
def get_back2():
    #do something
    return redirect(request.args.get('next', url_for('hello')))
#通用返回方法
def redirect_back(default='hello',**kwargs):
    target = request.args.get('next')
    print('Target is : ', target)
    if target and is_safe_url(target):
        return redirect(target)
    return redirect(url_for(default, **kwargs))
@app.route('/get_back_for_all')
def get_back_for_all():
    #do something
    return redirect_back()
#主页
@app.route('/index')
def index():
    return render_template('index.html')
#关于
@app.route('/about')
def about():
    return render_template('about.html')
#观影清单
@app.route('/watchlist')
def watchlist():
    movies = [
        {'name': 'My Neighbor Totoro', 'year': '1988'},
        {'name': 'Three Colours trilogy', 'year': '1993'},
        {'name': 'Forrest Gump', 'year': '1994'},
        {'name': 'Perfect Blue', 'year': '1997'},
        {'name': 'The Matrix', 'year': '1999'},
        {'name': 'Memento', 'year': '2000'},
        {'name': 'The Bucket list', 'year': '2007'},
        {'name': 'Black Swan', 'year': '2010'},
        {'name': 'Gone Girl', 'year': '2014'},
        {'name': 'CoCo', 'year': '2017'}
    ]
    user = {
        'username':'Grey Li',
        'bio':'A boy who loves movies and music.'
    }
    return render_template('watchlist.html',user=user,movies=movies)
#过滤器
@app.route('/filters')
def filters():
    namelist = ['Harry','Jack','Tom','Sam','Jone','Jane']
    numlist = [12,34,3,5,17,42,100,3,5,17,42,89,98,89]
    urlstr = 'http://www.baidu.com'
    return render_template('filters.html',namelist=namelist,numlist=numlist,urlstr=urlstr)

@app.route('/tests')
def tests():
    name = 'Jack'
    flash('I am flash , who is looking for me ?')
    return render_template('tests.html', name=name)

@app.route('/base')
def base():
    return render_template('base.html')
@app.route('/macrologin')
def macrologin():
    form = LoginForm()
    return render_template('login/mlogin.html', form=form)
@app.route('/tologin', methods=['GET','POST'])
def tologin():
    #form = LoginForm(meta={'locales':['en_US','en']})
    form = LoginForm()
    print('tologin method is : ' , request.method, ', submitted ? ' , form.validate_on_submit())
    '''
        表单实例化后，如果是GET请求，则会渲染模板。
        如果是POST，就调用validate()函数执行表单验证
    '''
    #if request.method == 'POST' and form.validate():
    '''
        Flask-WTF 提供的validate_on_submit()方法合并了请求方式判断及表单验证，所以以上写法可改为如下写法
    '''
        #pass
    if form.validate_on_submit():
        print('Do the post login action !!!')
        '''
            表单类的data属性是一个匹配所有字段与对应数据的字典，我们一般直接通过“ form.字段属性名.data ”的
            形式来获取对应字段的数据
        '''
        if form.username.data == 'admin' and form.password.data == '12345678':
            session.pop('loginfailed',None)
            session['loginuser'] = form.username.data
            return redirect(url_for('index'))
        else:
            session['loginfailed'] = '账号 / 密码错误!!!'
    return render_template('login/login.html', form=form)
@app.route('/signin',methods=['POST','GET'])
def signin():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    print('User name %s, password %s' %(username, password))
    if not username or not password:
        session['loginfailed'] = '账号 / 密码为空!!!'
    else:
        if username == 'admin' and password == '123456':
            session.pop('loginfailed',None)
            session['loginuser'] = username
            return redirect(url_for('index'))
        else:
            session['loginfailed'] = '账号 / 密码错误!!!'
    return redirect(url_for('tologin'))
#启动服务
if __name__ == '__main__':
    #Web服务器默认是对外不可见的，设置host参数为'0.0.0.0'使其对外可见
    app.run(host='0.0.0.0',port=8080,debug=True)