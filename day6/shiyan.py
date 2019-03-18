import math
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# 从flask_script包中导入Manager类，，用于管理项目
from flask_script import Manager
# 从flask_migrate包中导入Migrate，MigrateCommand，用于做数据库的迁移
from flask_migrate import Migrate, MigrateCommand
# 从sqlalchemy包中导入or_
from sqlalchemy import or_
# 从sqlalchemy包中导入func以便使用聚合函数
from sqlalchemy import func
# 导入pymysql 并将其视为 mysqldb
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/flask"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 为app指定启动模式
app.config['DEBUG'] = True

# 创建数据库应用实例 -db
db = SQLAlchemy(app)

# 创建Manager对象并指定要管理的应用(app)
manager = Manager(app)

# 创建Manager对象并指定关联的app和db
migrate = Migrate(app, db)
# 为manager增加子命令，允许做数据库迁移的子命令
# 为manager增加一个叫 db 的子命令，该子命令的具体操作由MigrateCommand来提供
manager.add_command('db', MigrateCommand)


# 创建实体类-Users，映射到数据库中叫users表
# 创建字段-id，主键，自增
# 创建字段-username，长度为80的字符串，不允许为空，值唯一，增加索引
# 创建字段-age，整数，允许为空
# 创建字段-email，长度为120的字符串，值唯一，不允许为空
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    # 重写__repr__方法去定义其展现形式
    def __repr__(self):
        return "<Users:%r>" % self.username


# 创建Student 实体类，表名：student  列：
#                 id，主键，整数，自增
#                 sname，姓名，长度为30并不允许为空的字符串
#                 sage，年龄，整数，不允许为空
#                 isActive，启用状态，布尔型，默认为True
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(30), nullable=False)
    sage = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)


# 创建Teacher 实体类，表名：teacher  列：
#                 id，主键，自增
#                 tname，姓名，长度为30并不允许为空的字符串
#                 tage，年龄，整数，不允许为空
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(30), nullable=False)
    tage = db.Column(db.Integer, nullable=False)
    # 增加一个属性-isActive，默认值为True
    isActive = db.Column(db.Boolean, default=True)
    # 增加一个列，引用自Course类(表)的主键(id)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)


# 创建Course 实体类，表名：course
#                 id，主键，自增
#                 cname，课程名称，长度为30并不允许为空的字符串
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30), nullable=False)
    # 增加关联属性和反向引用关系属性
    # 关联属性：在Course的对象中要通过哪个属性引用对应的所有的Teacher对象
    # 反向引用关系属性：在Teacher的对象中 要通过哪些属性引用对应的Course对象
    teachers = db.relationship('Teacher', backref='course', lazy='dynamic')

@app.route('/03-insert')
def jjfdkl():

    users = db.session.query(Users).first()
    print(users)
    count = db.session.query(Users).count()
    print("共有%d条数据" % count)

    # 3.查询过滤器函数-filter()
    # 3.1查询Users实体中，年龄大于19岁的人的信息
    users = db.session.query(Users).filter(Users.age > 19).all()
    for user in users:
        print("姓名：%s，年龄：%d" % (user.username, user.age))
    return "OK"



@app.route('/04-queryall')
def queryall_views():
    # 查询Users中的所有的数据
    users = db.session.query(Users).all()
    # 将数据发送到04-queryall.html中显示
    return render_template('04-queryall.html', users=users)


@app.route('/05-query_or')
def query_or_views():
    # 查询年龄大于30或者id大于1 的人的信息
    users = db.session.query(Users).filter(or_(Users.age > 30, Users.id > 1)).all()
    for user in users:
        print("姓名：%s，年龄：%d" % (user.username, user.age))
    return "Query Success!!!"


@app.route('/06-query_like')
def query_like_views():
    # 查询email中包含l的用户的信息
    users = db.session.query(Users).filter(Users.email.like('%l%')).all()
    for user in users:
        print("姓名：%s，邮箱：%s" % (user.username, user.email))
    return "Query Success!!!"


@app.route('/07-query_like_exer', methods=['GET', 'POST'])
def query_like_exer_views():
    uname = request.args.get('uname', '')
    # 如果uname不为空的话，则按照条件筛选
    if uname:
        users = db.session.query(Users).filter(Users.username.like('%' + uname + '%')).all()
    else:
        # 查询Users中所有的数据到模板中进行显示
        users = db.session.query(Users).all()
    return render_template('07-like.html', users=users, uname=uname)
    # # 查询姓名中包含指定数据的Users的信息
    # users = db.session.query(Users).filter(Users.username.like('%l%')).all()
    # for user in users:
    #     print("姓名：%s，邮箱：%s" % (user.username,user.email))


@app.route('/08-query_in')
def query_in():
    users = db.session.query(Users).filter(Users.age.in_([18, 20])).all()
    for user in users:
        print("姓名：%s，邮箱：%s" % (user.username, user.email))
    return "成功"


# 使用 filter_by 查询Users 中isActive为True的用户的信息
@app.route('/09-filter_by')
def filter_by_views():
    users = db.session.query(Users).filter_by(isActive=True).all()
    for user in users:
        print("姓名：%s，邮箱：%s" % (user.username, user.email))
    return "成功"


@app.route('/10-limit')
def limit_views():
    # 取users表中前2条数据
    users = db.session.query(Users).limit(2).all()
    for user in users:
        print("姓名：%s，邮箱：%s" % (user.username, user.email))
    return "成功"


