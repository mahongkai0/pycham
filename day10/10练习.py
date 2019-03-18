from flask import Flask, render_template, request,redirect #分别导入flask  渲染模板函数  请求函数  重定向函数
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/ajax"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#设置自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# 导入pymysql 并将其视为 mysqldb
import pymysql
pymysql.install_as_MySQLdb()


db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id= db.Column(db.Integer,primary_key=True)

    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(30))
    nickname=db.Column(db.String(30))

@app.route('/01-reg',methods=['POST','GET'])
def fj():
    if request.method == 'GET':
        return render_template('01-reg.html')
    else:
        user = Users()
        user.uname = request.form['uname']
        user.upwd= request.form['upwd']
        user.nickname=request.form['nickname']
        db.session.add(user)
        return "注册成功"

@app.route('/01-checkuname')
def changeuname_bif():
    #接受参数
    uname = request.args['uname']
    #验证结果是否存在
    u = Users.query.filter_by(uname=uname).first()

    #根据结果是否给出返回值
    if u :
        return "用户名已存在"
    else:
        return "通过"






@app.route('/02-post',methods=['POST','GET'])
def post_view():
    if request.method == 'GET':
        return render_template('02-post.html')
    else:
        uname = request.form['uname']
        return "欢迎"+uname







db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
