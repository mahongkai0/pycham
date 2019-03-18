



from flask import Flask, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/ajax"
# 取消SQLALchemy 的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置自动提交
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 为app指定启动模式
app.config["DEBUG"] = True
# 创建数据库应用实例 -db
db = SQLAlchemy(app)

# 创建Manager对象并制定要管理的应用(app)
manager = Manager(app)
# 创建一个 Migrate对象,并指定关联的app和db
migrate = Migrate(app, db)
# 为manager增加子命令,允许做数据库迁移的子命令
# 为manager增加一个叫 db 的子命令,该子命令的具体操作将由MigrateCommand来提供
manager.add_command('db', MigrateCommand)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(30))
    nickname = db.Column(db.String(30))

    def to_dict(self):
        """
        将当前类的属性封装成一个字典并响应
        :return:将属性封装成字典后的表现
        """
        dic={
            "id":self.id,
            "uname":self.uname,
            "upwd":self.upwd,
            "nickname":self.nickname
        }
        return dic

@app.route('/00-homework')
def hello_world():
    #12.查询user表中所有的数据
    users = Users.query.all()
    #2。循环遍历列表取出每个对象转换成字典再放入另一个列表中
    l = []
    for u in users:
        l.append(u.to_dict())
    #3. 将列表转换成JSON串再响应
    return  json.dumps(l)


@app.route('/01-load')
def load_kkk():
    return "这是使用$obj.load加载回来的数据"

@app.route('/02-get')
def get_vie():
    #1.接受参数 uname
    uname = request.args['uname']
    #2. 按照uname查询对应的数据
    users= Users.query.filter_by(uname = uname).all()
    #3 将数据转换成json串进行响应
    l=[]
    for u in users:
        l.append(u.to_dict())
    return json.dumps(l)

@app.route('/03-lianxi')
def lianxi_r():
    #接受前段传递过来的参数
    #模糊查询 查询 users表中uname为开头的
    #将数据转换为json串经信号鲜花与

    uname = request.args['uname']
    users = Users.query.filter(Users.uname.like(uname+"%")).all()
    l=[]
    for u in users:
        l.append(u.to_dict())
    return json.dumps(l)


@app.route('/04-ajax')
def hkj():
    users = Users.query.all()
    l = []
    for u in users:
        l.append(u.to_dict())
    return json.dumps(l)


@app.route("/06-cross")
def  cross_fvk():
    #return "console.log('成功访问到/06-cross地址')"
    #return "$('#show').html('成功访问到/06-crosee地址')"
    return "print_msg('成功访问到/06-crosee地址')"




if __name__ == '__main__':
    app.run(debug=True)

















