from flask import Flask
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
