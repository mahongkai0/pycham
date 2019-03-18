from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 用于管理项目
from flask_script import Manager

#用于数据库的迁移
from flask_migrate import Migrate ,MigrateCommand

# 导入pymysql 并将其视为 mysqldb
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/blog"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库应用实例 -db
db = SQLAlchemy(app)

#为app指定app.config['DEBUG']=True
app.config['DEBUG']=True


#创建Manager对象并指定要管理的应用（app）
manager=Manager(app)

#创建Migrate对象并指定关联的app 和db
migrate=Migrate(app,db)

#为manager增加子命令，允许做数据库迁移的子命令
#准备为manager增加一个叫 随便起db 的子命令 该子命令的具体操作将由MigrateCommand来提供
manager.add_command('db',MigrateCommand)

#id uname(50),email(200),url(200) upwd(200)
class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    uname=db.Column(db.String(50),nullable=False,index=True)
    email=db.Column(db.String(200),nullable=False)
    url=db.Column(db.String(200),nullable=False)
    upwd=db.Column(db.String(200),nullable=False)


#
@app.route('/')
def index():
    return "这是我的Flask"




if __name__ == "__main__":
    manager.run()