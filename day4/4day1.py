from flask import Flask,render_template,request
import os,datetime
app = Flask(__name__)


@app.route('/01-file',methods=['GET','POST'])
def file_views():
    if request.method =='GET':
        return render_template('01-file.html')
    else:
        #1.从缓存区取名称为picture的文件 （name的值）
        #2.将获取的文件使用其原始名称保存至static目录中
        if 'picture' in request.files:
            f= request.files['picture']
            #2.1获取文件名
            #fname=f.filename

            #将采用年月日时分秒微秒.扩展名来给文件命名以解决重名问题
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            print(ftime)
            #获取文件的扩展名
            ext=f.filename.split('.')[-1]
            fname=ftime + '.'+ ext

            print("上传的文件名为："+fname)
            #2.2保存在static中
            # f.save('static/'+fname)
            #使用绝对路径保存
            basedir=os.path.dirname(__file__)
            print(basedir)
                            #print("basedir"+basedir)
            upload_path=os.path.join(basedir,'static',fname)
                                 #print(upload_path)
            f.save(upload_path)
        uname=request.form['uname']
        print('用户名'+ uname)
        return "文件上传成功"







if __name__ == '__main__':
    app.run(debug=True)


