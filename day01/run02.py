#从flask包中导入Flask
from flask import  Flask


app=Flask(__name__)


@app.route('/login')
def gg():
    return "欢迎访问登陆界面"
@app.route('/register')
def hh():
    return "欢迎访问注册界面"

@app.route('/news/<year>')
def news(year):
    return "<h1>一天帅"+year+"次</h1>"




@app.route('/news/<year>/<month>')
def d(year,month):
    return "<h1>年份"+year+"."+month+"</h1>"



@app.route('/info/<name>/<int:age>')
def ms(name,age):

    return "姓名:%s,年龄:%d" % (name,age)


#127.0.0.1:5000/category
#127.0.0.1:5000/cate

@app.route('/category')
@app.route('/cate')
def cate():
    return "这是category对应的视图"



1
1
1


#运行Flask的应用（启动flask的服务） 默认在本机开启的端口是5000
#debug=True 将以调试模式的方式启动服务（开发环境视同True 生产环境重病使用False）
if __name__== "__main__":
        app.run(debug=True)





