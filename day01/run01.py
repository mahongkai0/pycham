#从flask包中导入Flask
#from flask import  Flask

#将当前运行的主程序构建成Flask的应用
#以便接受用户的请求（request） 并给出相应（response）
from flask import Flask

app=Flask(__name__)

#@app.route() 是flask中的路由定义 主要定义用户的访问路径
#‘/’表示的是整个网站的根路径
#def index（）表示的是匹配到 @app.route（） 后的访问路径之后的处理程序--视图函数
#所有的函数中必须要有一个return return的后面可以是一个字符串或相应对象  表示的是要响应
#给客户端浏览器的内容是什么
@app.route('/')
def index():
    return "<script>alert('这是我的第一个Flask Demo')</script>"
@app.route('/thow')
def show():
    return "这是我的show访问路径"


#运行Flask的应用（启动flask的服务） 默认在本机开启的端口是5000
#debug=True 将以调试模式的方式启动服务（开发环境视同True 生产环境重病使用False）
if __name__== "__main__":
        app.run(debug=True)












