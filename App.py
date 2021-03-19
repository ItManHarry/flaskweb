from flask import Flask,request

app = Flask(__name__)

@app.route('/hello')
def hello():
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
    return '<h1>Hello flask .</h1>'

'''
    1. 绑定多个路由
    2. 动态路由
    3. 设置参数默认值
'''
@app.route('/greet')
@app.route('/greet/<name>')
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

if __name__ == '__main__':
    app.run(port=8080,debug=True)