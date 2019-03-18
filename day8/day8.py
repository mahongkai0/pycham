from flask import Flask, make_response, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '文本'

@app.route('/00-test')
def tes_h():
    return "测试地址"





@app.route('/01-setcookies')
def sercookes():
    #通过make_response构建响应对象
    #保存名称为uname  值为张三,存期为1年
    #保存一个名称为upwd  值为123456的cookies  没有保存时长



    resp = make_response("保存cookies成功")

    resp.set_cookie('uname','张三',60*60*24*365)
    resp.set_cookie('upwd','123456')
    # 响应 保存 cookies成功
    return resp

##
@app.route('/02-login',methods=['GET','POST'])
def login_views():
    if request.method =='GET':
      if 'uname' in request.cookies and 'upwd' in request.cookies:
           #获取usename和upwd的值
           uname = request.cookies['uname']
           upwd=request.cookies['upwd']
           #判断值是否为admin
           if uname == 'admin' and upwd=='admin':
               return "欢迎"+uname
      return render_template('02-login.html')

    else:
        #接受用户名和密码
        uname=request.form['uname']
        upwd=request.form['upwd']

        #判断用户名密码正确性
        if uname == 'admin' and upwd == 'admin':
            resp= make_response('登陆成功')
            if 'isSaved' in request.form:
                max_age=60*60*24*365
                resp.set_cookie('uname',uname,max_age)
                resp.set_cookie('upwd', upwd, max_age)

            return resp

        #如果都为admin 判断是否要记住密码
        #   如果记住密码则保存尽cookies
        #如果不是 提示错误

        else:
            return "用户名和密码不正确: <a href='/02-login'>登录</a>"



@app.route('/03-getcookie')
def getcookies_vie():
    print(request.cookies)
    if 'uname' in request.cookies:
        print("用户名"+request.cookies['uname'])
    if 'upwd' in request.cookies:
        print("密码" + request.cookies['upwd'])
    return "获取cookies成功"


@app.route('/04-setsession')
def setsession_v():
    session['uname'] = '小泽'
    session['upwd'] = "123456"
    return "添加session成功"
@app.route('/05-getsession')
def getssion_bk():

    if 'uname' in session and 'upwd' in session:
        return "用户名：%s，密码：%s" %(session['uname'],session['upwd'])
    return "session中没有数据"

@app.route('/06-login',methods=['POST','GET'])
def login_bb():
    if request.method =='GET':
        if 'uname' in session and 'upwd' in session:
            uname = session['uname']
            return "欢迎"+uname+"来到这里"
        return render_template('06-login.html')
    else:
        uname = request.form['uname']
        upwd=request.form['upwd']


        if uname == 'admin' and upwd=='admin':
            session['uname'] = uname
            session['upwd'] = upwd
            return "成功"
        return "失败"




if __name__ == "__main__":
    app.run(debug=True)











