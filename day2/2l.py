from flask import Flask, render_template

app=Flask(__name__)



@app.route('/01-temp')
def temp():
    '''这个的目的是演示模板的渲染和响应 ：return 响应内容'''
    name='张三'
    age=30
    gender='男'
    return render_template('01-temp.html',name=name,age=age,gender=gender)
if __name__=="__main__":
    app.run(debug=True)







