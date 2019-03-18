from flask import Flask, request, render_template
import datetime, os

app = Flask(__name__)


@app.route('/02-lianxi', methods=['GET', 'POST'])
def lianxi():
    if request.method == 'GET':
        return render_template('02-lianxi.html')
    else:

        title = request.form['title']

        type = request.form['type']
        content = request.form['content']

        print("标题为:" + title)
        print("类型为：" + type)
        print("内容为:" + content)
        # 处理上传的文件
        if 'picture' in request.files:
            # 1.获取文件
            f = request.files['picture']
            # 2.根据文件的名称对应至对应的目录处
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename = ftime + "." + ext
            #获取他的绝对路径

            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, 'static/upload', filename)
            print("图片路径为：", upload_path)
            # j3.将文件保存至对应的目录处
            f.save(upload_path)
        return "博客发表成功"


if __name__ == '__main__':
    app.run(debug=True)
