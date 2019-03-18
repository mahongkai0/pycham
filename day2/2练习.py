from flask import Flask, render_template, request

app = Flask(__name__)


# 127.0.0.1:5000/
# 127.0.0.1:5000/login
# 127.0.0.1:5000/register
# 127.0.0.1:5000/list
# 127.0.0.1:5000/info

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    # 根据request.method判断用户的请求意图
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print("用户名：%s，密码：%s" % (username, password))

        return "接受数据成功"


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/list')
def list_v():
    return render_template("list.html")


@app.route('/info')
def info_v():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True)
