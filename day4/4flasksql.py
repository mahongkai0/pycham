from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 导入pymysql 并将其视为 mysqldb

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/flask"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# 创建数据库应用实例 -db
db = SQLAlchemy(app)



# 创建实体类-Users，映射到数据库中叫users表
# 创建字段-id，主键，自增
# 创建字段-username，长度为80的字符串，不允许为空，值唯一，增加索引
# 创建字段-age，整数，允许为空
# 创建字段-email，长度为120的字符串，值唯一，不允许为空
# class Users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False, unique=True, index=True)
#     age = db.Column(db.Integer, nullable=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)


class Student(db.Model):
    __tablename__='student'
    id= db.Column(db.Integer,primary_key=True,autoincrement=True) #自增可以不用写
    sname=db.Column(db.String(30),nullable=False)
    sage= db.Column(db.Integer,nullable=False)
    isActive=db.Column(db.Boolean,default=True)
    #增加一个列 引用自Course类（表）的主键（id）


class Teacher(db.Model):
    __tablename__='teacher'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tname=db.Column(db.String(30),nullable=False)
    tage = db.Column(db.Integer,nullable=False)
    isActive =db.Column(db.Boolean,default=True)
    # 增加一个列 引用自Course类（表）的主键（id）
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable=True)


class Course(db.Model):
    __tablename__='course'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname=db.Column(db.String(30),nullable=True)
    #增加关联属性和反向引用关系属性
    #关联属性：在Course的对象中 要通过哪个属性引用对应的所有Teancher对象
    #反向引用关系属性：在Teacher的对象中要通过哪个属性引用对应的Course对象中
    teachers = db.relationship(
            'Teacher',
            backref='cours',
            lazy='dynamic'
        )

@app.route('/16-regteacher')
def regteacher():
    pass



#删除所有的数据表
db.drop_all()




# 将创建好的实体类映射回数据库，生成表
# (前提：数据表不存在)
db.create_all()



@app.route('/')
def index():
    return "这是我的Flask"
if __name__ == "__main__":
    app.run(debug=True)



















