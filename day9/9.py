from flask import Flask, make_response, render_template, request, session

app = Flask(__name__)

@app.route('/00-test')
def tes_h():
    return "测试地址"


@app.route('/01-ajax-get')
def tes_hfff():
    return "这是我的第一个ajax请求"


if __name__ == "__main__":
    app.run(debug=True)
