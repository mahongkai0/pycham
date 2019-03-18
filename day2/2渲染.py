from flask import Flask,render_template

app = Flask(__name__)

@app.route('/02-var')
def ma():
    book='钢铁是怎样'
    peole='李白'
    house='bejing'
    time='196-12-12'
    return render_template('02-var.html',book=book,peole=peole,house=house,time=time)

@app.route('/3-var')
def var03():
    '''演示允许传递到模板中变量的数据类型'''
    uname='一鸣'
    uage=16
    salary=350
    list=["青岛","卡卡西","佐助"]
    tup=["贪","嗔","痴","恨"]
    dic={"W":'微老板',"LMM":'吕蒙蒙',"s":'山海经'}
    person=Person()
    person.name="狮王，金毛"
    return render_template('3-var.html',params=locals())
#uname=uname,uage=uage,salary=salary,list=list,tup=tup,dic=dic,person=person


@app.route('/04.filter')
def filter_views():
    salary=-785
    name="jiayou xi"
    msg= "dolorsitamet,consectetur adipisi"
    return render_template('04-filter.html',salary=salary,name=name,msg=msg)


#for
@app.route('/05-for')
def for_view():
    list=["陈圆圆","古天乐","渣渣辉"]
    return render_template('05-for.html',list=list)



#宏
@app.route('/06-macro')
def macro_1():
    list=['a','b','c','d']
    return render_template('06-macro.html',list=list)

@app.route('/static')
def static_1():
    return render_template('07-static.html')




class Person(object):
    name=None
    def show(self):
        return "my name is " + self.name




if __name__ == "__main__":
    app.run(debug=True)







