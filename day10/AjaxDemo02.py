from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/ajax"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(30))
    nickname = db.Column(db.String(30))

db.create_all()

@app.route('/01-reg',methods=['POST','GET'])
def register_views():
    if request.method == 'GET':
        return render_template('01-reg.html')
    else:
        user = Users()
        user.uname = request.form['uname']
        user.upwd = request.form['upwd']
        user.nickname = request.form['nickname']

        db.session.add(user)

        return "注册成功"

@app.route('/01-checkuname')
def checkuname_views():
    #1.接收参数
    uname = request.args['uname']
    #2.验证数据是否存在
    u=Users.query.filter_by(uname=uname).first()
    #3.根据结果给出返回值
    if u :
        return "用户名称已存在"
    else:
        return "通过"

@app.route('/02-post',methods=['GET','POST'])
def post_views():
    if request.method == 'GET':
        return render_template('02-post.html')
    else:
        uname = request.form['uname']
        return "欢迎:"+uname

if __name__ == '__main__':
    app.run(debug=True)
