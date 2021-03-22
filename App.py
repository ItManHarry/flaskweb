from flask import Flask,request,make_response,jsonify,redirect,url_for,session,g
import json
import os
app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY', 'secretkey0001')
#钩子函数
@app.before_first_request
def init():
    print('Web App Start, Do The Init Action!!!')

@app.before_request
def reqintercepter():
    g.name = request.args.get('name')
    print('Intercept every request!!!')

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
    return redirect(url_for('hello'))
if __name__ == '__main__':
    app.run(port=8080,debug=True)