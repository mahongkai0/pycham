from flask import Flask, render_template, request
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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/flask"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#设置自动提交
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True


#为app指定app.config['DEBUG']=True
app.config['DEBUG']=True
# 创建数据库应用实例 -db
db = SQLAlchemy(app)


#创建Manager对象并指定要管理的应用（app）
manager=Manager(app)

#创建Migrate对象并指定关联的app 和db
migrate=Migrate(app,db)

#为manager增加子命令，允许做数据库迁移的子命令
#准备为manager增加一个叫 随便起db 的子命令 该子命令的具体操作将由MigrateCommand来提供
manager.add_command('db',MigrateCommand)





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
#     #增加一个属性 isActive 默认值为True
#     isActive=db.Column(db.Boolean,default=True)
#     na = db.Column(db.Boolean, default=True)
    # 重写__repr__方法去定义其展现形式 为了拿到数组
    def __repr__(self):
        return "<Users:%s>" % self.username

#
@app.route('/')
def index():
    return "这是我的Flask"

@app.route('/01-add')
def add_views():
    users=Users()
    users.username="卢泽马瑞亚"
    users.age= 31
    users.email = 'maria@163.com'
    db.session.add(users)
    db.session.commit()
    return "Register Users Success!"

@app.route('/02-register',methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        return render_template("02-register.html")
    else:

        username=request.form['username']
        age=request.form['age']
        email=request.form['email']
        #如果为True证明激活被点击了

        # isActive= False
        # if 'isActive' in request.form:
        #     isActive=True

        isActive= 'isActive' in request.form

        users = Users()
        users.username=username
        users.email=email
        users.isActive=isActive
        db.session.add(users)
        db.session.commit()
        return "注册成功"
@app.route('/03-query')
def query_views():
    #通过db。cession.query 查询、
    #query=db.session.query(Users.id,Users.email,Users.age)
    query=db.session.query(Users)
    print('query',query)
    print('type:',type(query))

   #2.c查询执行函数
    users=db.session.query(Users).all()
    for u in users:

        print("姓名：%s，年龄：%s,邮箱：%s" % (u.username, u.age,u.email))
        print(users)

        count=db.session.query(Users).count()
        print("User中有%d数据" % count)

        #chaxun 过滤器函数 filter（）
        #查询Users实体中 年龄大于30
        usersk=db.session.query(Users).filter(Users.age>30).all()
        for user in usersk:
            print("姓名：%s，年龄：%d" %(user.username,user.age))



    return "Query Success"



@app.route('/04-queryall',methods=['POST','GET'])
def queryall_views():
    #查询Users中的所有的数据
    users=db.session.query(Users).all()
    #将数据发送到04-queryall.html中
    return  render_template('04-queryall.html',users = users)



if __name__ == "__main__":
    #app.run(debug=True)
    #通过manager启动服务
    manager.run()

    #通过 manger启动服务
    #python3 run01.py   runserver
    #问题一  无法指定调试模式（debug=True）
    #解决方案  app.config['DEBUG']=True
    #问题二：无法指定启动主机地址（host=0.0.0.0）
    #解决方案  ：  python3 run01.py -- host 0.0.0.0
    #问题三  无法指定启动端口  （post=5555）
    #解决方案  python3 run01.py runserver --port 5555
    #runserver - -host 127.0.0.1 - -port 5000
    #可看 python run.py     python run.py db init
#Target database is not up to date.












