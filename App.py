from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return '<h1>Hello flask .</h1>'

'''
    1. 绑定多个路由
    2. 动态路由
    3. 设置参数默认值
'''
@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='Programmer'):
    return '<h1>Hello , %s !</h1>' %name

if __name__ == '__main__':
    app.run(port=8080,debug=True)