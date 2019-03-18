from flask import Flask,url_for

app=Flask(__name__)


# @app.route('/')
# @app.route('/index')
# @app.route('/<int:num>')
# @app.route('/index/<int:num>')
#
# def index(num=1):
#
#         return "您当前看到的页数为:%s" %(num)


@app.route('/')
def index():
    # #return "<a href='/login'>登陆</a>"#####正向解析
    url_login=url_for('login')
    # print("地址为",url_login)
    return "<a href='%s'>登陆</a>"% url_login


#@app.route('/login')#####正向解析
    # url_show=url_for('show',name="小泽")
    # return "<a href='%s'>显示</a>" %url_show
    #

@app.route('/kf/login/uesr/admin')
def login():
    return "欢迎来到登陆页面"

@app.route('/d/show/hhhf/<name>')
def show(name):
    return  "姓名为:%s" %name





if __name__=="__main__":
    app.run(debug=True)








