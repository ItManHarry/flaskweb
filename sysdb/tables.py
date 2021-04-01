from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
'''
    常用数据连接URI格式
    PostgreSQL        postgresql://username:password@host/databasename
    MySQL             mysql://username:password@host/databasename
    Oracle            oracle://username:password@host:port/sidname
    SQLite(UNIX)      sqlite:////absolute/path/to/foo.db
    SQLite(Windows)   sqlite:///absolute\\path\\to\\foo.db或r’sqlite:///absolute\path\to\foo.db'
    SQlite(内存型）     sqlite:///或sqlite:///:memory:
'''
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLITE_DATABASE_URL', 'sqlite:///'+os.path.join(app.root_path, 'data.db'))
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
'''
    默认情况下， Flask-SQLAlchemy会根据模型类的名称生成一个表名称，生成规则如下：
    Message --> message ＃单个单词转换为小写
    FooBar  --> foo_bar ＃多个单词转换为小写并使用下划线分隔
'''
class Note(db.Model):
    id = db.Column(db.String, primary_key=True)
    title=db.Column(db.String)
    body= db.Column(db.Text)
    def __repr__(self):
        return '<Note %r>' %self.body

def init_db():
    db.create_all()

__all__ = ['db','init_db','Note']