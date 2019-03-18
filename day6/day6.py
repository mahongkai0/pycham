from flask import Flask, render_template, request,redirect #分别导入flask  渲染模板函数  请求函数  重定向函数
from flask_sqlalchemy import SQLAlchemy
#从sqlalchemy包中导入or_
from sqlalchemy import or_, func
import math
# 用于管理项目
from flask_script import Manager


#用于数据库的迁移
from flask_migrate import Migrate ,MigrateCommand

# 导入pymysql 并将其视为 mysqldb
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
# 通过app指定连接数据库的信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/flask"
# 取消SQLAlchemy的信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#设置自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True


#为app指定app.config['DEBUG']=True
app.config['DEBUG']=True
# 创建数据库应用实例 -db
db = SQLAlchemy(app)


#创建Manager对象并指定要管理的应用（app）
manager=Manager(app)

#创建Migrate对象并指定关联的app 和db
migrate=Migrate(app,db)

#为manager增加子命令，允许做数据库迁移的子命令
#准备为manager增加一个叫 随便起db 的子命令 该子命令的具体操作将由MigrateCommand来提供
manager.add_command('db',MigrateCommand)


url_ref = None


# 创建实体类-Users，映射到数据库中叫users表
# 创建字段-id，主键，自增
# 创建字段-username，长度为80的字符串，不允许为空，值唯一，增加索引
# 创建字段-age，整数，允许为空
# 创建字段-email，长度为120的字符串，值唯一，不允许为空
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isActive=db.Column(db.Boolean,default=True)
    #做与wifr类之间的一对一的关联属性和反向引用关系属性
    wife=db.relationship('Wife',backref='user',uselist=False)

#     #增加一个属性 isActive 默认值为True
#     isActive=db.Column(db.Boolean,default=True)
#     na = db.Column(db.Boolean, default=True)
    # 重写__repr__方法去定义其展现形式 为了拿到数组

    
    def __repr__(self):
        return "<Users:%s>" % self.username




#
#
class Student(db.Model):
    __tablename__='student'
    id= db.Column(db.Integer,primary_key=True,autoincrement=True) #自增可以不用写
    sname=db.Column(db.String(30),nullable=False)
    sage= db.Column(db.Integer,nullable=False)
    isActive=db.Column(db.Boolean,default=True)
    #增加一个列 引用自Course类（表）的主键（id）
#
#
class Teacher(db.Model):
    __tablename__='teacher'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tname=db.Column(db.String(30),nullable=False)
    tage = db.Column(db.Integer,nullable=False)
    # 增加一个列 引用自Course类（表）的主键（id）
    isActive = db.Column(db.Boolean, default=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable=True)

#
class Course(db.Model):
    __tablename__='course'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname=db.Column(db.String(30),nullable=True)
    #增加关联属性和反向引用关系属性
    #关联属性：在Course的对象中 要通过哪个属性引用对应的所有Teancher对象
    #反向引用关系属性：在Teacher的对象中要通过哪个属性引用对应的Course对象中
    teachers = db.relationship( 'Teacher', backref='course',lazy='dynamic')
    #增加对Student类的多对多操作 （关联属性和反向引用关系属性）
    students= db.relationship(
        "Student",
        secondary="student_course",
        lazy="dynamic",
        backref=db.backref(
            "course",
            lazy="dynamic"
        )
    )




#增加一个实体类 wife 要与Users实体类做一对一的关联映射
class Wife(db.Model):
    __tablename__='wife'
    id = db.Column(db.Integer,primary_key=True)
    wname = db.Column(db.String(20))
    wage=db.Column(db.Integer)
    #增加外键 表示与User表中一对一关系
    users_id = db.Column(db.Integer,db.ForeignKey('users.id'),unique=True)


#实体类 StudentCourse 表示Student和Course之间的第三张关联表
class StudentCourse(db.Model):
    __tablename__='student_course'
    id = db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))







@app.route('/19-addwife')
def addwife_views():
    # wife=Wife()
    # wife.wname='Maria夫人'
    # wife.wage=30
    # wife.users_id=3
    # db.session.add(wife)

#方式2  利用反向引用关系添加关联数据
    user = Users.query.filter_by(id=5).first()
    wife=Wife()
    wife.wname = 'kk'
    wife.wage = 30
    wife.user=user
    db.session.add(wife)
    return "good"
@app.route('/20-oto',methods=['POST','GET'])
def oto_vi():
    if request.method == 'GET':
        #查询Users中的所有数据
        users=Users.query.all()
        return render_template('20-oto.html',users=users)

        #查询Users中的所有数据
    else:
        #接受前段数据
        wname= request.form['wname']
        wage=request.form['wage']
        user_id=request.form['user']
        #判断user_id在wife表中是否存在
        user=Wife.query.filter_by(users_id=user_id).first()
        if user:
            #user_id 已存在
            return "user已经存在"
        else:
            #不存在则可以做插入
            wife=Wife()
            wife.wname=wname
            wife.wage=wage
            wife.users_id=user_id
            db.session.add(wife)
            return "注册人成功"

@app.route('/21-oto')
def oto21_vie():
    wifes=Wife.query.all()

    return render_template('21-oto.html',wifes=wifes)


@app.route('/22-stu')
def hmtv_vie():
    #创建student对象 并保存在数据库

    stu = Student()
    stu.sname='鸣人'
    stu.sage=16
    stu.isActive=True
    db.session.add(stu)
    db.session.commit()
    # 查询出id为1的course信息，并插入第三张关联表中

    course= Course.query.filter_by(id=1).first()
    ##从编程的角度来+
    course.students.append(stu)
    return "插入关联数据成功"


@app.route('/22-mtm',methods=['GET','POST'])
def mtm_view():
    if request.method =='GET':
        courses=Course.query.all()
        return render_template('22-mtm.html',courses=courses)
    else:
        sname=request.form['sname']
        sage=request.form['sage']
        stu=Student()
        stu.sname=sname
        stu.sage=sage
        db.session.add(stu)
        db.session.commit()
        #获取所有的course值
        course_id= request.form.getlist('courses')
        print(course_id)
        #获取到相关的course对象
        list= Course.query.filter(Course.id.in_(course_id)).all()
        #循环遍历list 得到每个course并append到study中
        for course in list:
            course.students.append(stu)
        return "注册成功"
@app.route('/24-mtm-query')
def mtm_query():
    #通过course查student
    # course=Course.query.filter_by(id=1).first()
    # students=course.students.all()
    # print("课程名称："+course.cname)
    # print("学员信息")
    # for s in students:
    #     print("姓名：%s，年龄：%d"%(s.sname,s.sage))
    #
    ## 查询 id为2的学员锁选择的课程
    ## 通过student查courese
    student = Student.query.filter_by(id=1).first()
    courses= student.course.all()
    #print(courses)

    for x in courses:

        print("所学名称"+x.cname)

    return "OK"













#一对多
@app.route('/18-reg')
def regteacher_k():
    #方案1;通过外键设定关联数据
    teacher = Teacher()
    teacher.tname = '魏老师'
    teacher.tage = 47
    teacher.isActive = True
    teacher.course_id = 1
    db.session.add(teacher)
    


    ######方案2 通过反向引用关系属性
    course = Course.query.filter_by(id=2).first()
    ####声明一个Teacher对象 并将course赋值给Teacher对象的course属性
    teacher = Teacher()
    teacher.tname='王丹波'
    teacher.tage=36
    teacher.isActive=True
    teacher.course = course
    db.session.add(teacher)


    return "增加老师成功"

@app.route('/17-query')
def query17_views():
    #通过teacher对象查询对应的course信息
    teacher= Teacher.query.filter_by(tname="蒙蒙").first()
    print(teacher)
    #通过teacher.course 属性获取对应的course
    print("老师："+teacher.tname)
    print("所教课程:"+teacher.course.cname)

    #2.通过course查询对应的老师们
    course=Course.query.filter_by(id=2).first()
    print(course.teachers)
    print(type(course.teachers))
    teachers=course.teachers.all() #得到全部数据
    for tea in teachers:
        print("姓名：%s，课程：%s"%(tea.tname,tea.course.cname))

    return "Query OK"

@app.route('/18-query')
def query_viess():
    #获取所有课程
    courses=Course.query.all()

    #接受前段传过来的id值
    #有id的话则查询对应的课程老师
    #没有id'的话则查询所有的老师
    if 'id' in request.args:
        #c查询对应课程的老师
        id = request.args.get('id')
        teachers=Teacher.query.filter_by(course_id=id).all()
    else:
        id = 0
        #查询所有老师
        teachers=Teacher.query.all()
    #不管走谁都有teachers 所有就可以串过去
    return render_template('18-query.html',courses=courses,teachers=teachers,id=int(id))






@app.route('/')
def index():
    return "这是我的....Flask"

@app.route('/01-add')
def add_views():
    users=Users()
    users.username="shan马瑞亚"
    users.age= 16
    users.email = 'maria@162.com'
    db.session.add(users)
    
    return "Register Users Success!"

@app.route('/02-register',methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        return render_template("02-register.html")
    else:

        username=request.form['username']
        age=request.form['age']
        email=request.form['email']
        #如果为True证明激活被点击了

        # isActive= False
        # if 'isActive' in request.form:
        #     isActive=True

        isActive= 'isActive' in request.form

        users = Users()
        users.username=username
        users.email=email
        users.isActive=isActive
        db.session.add(users)
        
        return "注册成功"
@app.route('/03-query')
def query_views():
    #通过db。cession.query 查询、
    #query=db.session.query(Users.id,Users.email,Users.age)
    query=db.session.query(Users)
    print('query',query)
    print('type:',type(query))

   #2.c查询执行函数
    users=db.session.query(Users).all()
    for u in users:

        print("姓名：%s，年龄：%s,邮箱：%s" % (u.username, u.age,u.email))
        print(users)

        count=db.session.query(Users).count()
        print("User中有%d数据" % count)

        #chaxun 过滤器函数 filter（）
        #查询Users实体中 年龄大于30
        usersk=db.session.query(Users).filter(Users.age>30).all()
        for user in usersk:
            print("姓名：%s，年龄：%d" %(user.username,user.age))



    return "Query Success"



@app.route('/04-queryall',methods=['POST','GET'])
def queryall_views():
    #查询Users中的所有的数据
    users=db.session.query(Users).all()
    #将数据发送到04-queryall.html中
    return  render_template('04-queryall.html',users = users)


@app.route('/05-queryor')
def query_or():
    #查询年龄大于40 或者id 》1
    users=db.session.query(Users).filter(or_(Users.age>40,Users.id>1)).all()
    for u in  users:
        print("id:%d,姓名：%s，年龄：%d" % (u.id,u.username,u.age))
        db.session.query(Users).filter(Users.id == 1).first()
        return "Query Success 查询完毕"

@app.route('/06-querylike')
def querylike():
    userlike=db.session.query(Users).filter(Users.email.like('%maria%')).all()
    print(userlike)
    for u in userlike:
        print("id:%d,姓名：%s，年龄：%d" % (u.id, u.username, u.age))
    return "Query Success or查询完毕"



@app.route("/07-query_like_exer")
def query_like_exer_views():
    uname = request.args.get('uname', "")
    #如果uname不为空的话,则按照条件筛选
    if uname:
        users = db.session.query(Users).filter(Users.username.like("%"+uname+"%")).all()
        #users=db.session.query(Users).filter(or_(Users.))
    else:
        #否则查询所有数据
        users = db.session.query(Users).all()

    #查询users中所有的数据到模板中显示
    #users = db.session.query(Users).all()
    return render_template("07-like.html",users=users,uname=uname)


@app.route('/08-in')
def in_d():
    d=db.session.query(Users).filter(Users.age.in_([31,30])).all()
    for x in d:
        print("姓名：%s，年龄：%s" %(x.username,x.age))
    return "jieshu"



@app.route('/09-between')
def in_x():
    d=db.session.query(Users).filter(Users.age.between(15,30)).all()
    for x in d:
        print("姓名：%s，年龄：%s" %(x.username,x.age))
    #print(db.session.query(Users).filter_by(isActive=True).all())
    return "jieshu"

###offset也在
@app.route('/10-limit')
def limit_b():
    #users=db.session.query(Users).limit(2)
    users = db.session.query(Users).offset(1).limit(1).all()
    for x in users:
        print("姓名：%s，年龄：%s，邮箱：%s"%(x.username,x.age,x.email))
    return "dd"

@app.route('/10-page')
def page_view():
    #每页要显示的记录数量
    pageSize=2

    #接受前段传递过来的参数-apge 如果没有传递过来 则默认为1 并保存在page变量中
    page=int(request.args.get('page',1))

    #查询第page页的数据
    #跳过（page-1）*pabgSize 显示pageSize
    ost=(page - 1) * pageSize
    users=db.session.query(Users).offset(ost).limit(pageSize).all()

    # 计算尾页
    # 根据pageSize记录和总记录数尾页页码
    count_all = db.session.query(Users).count()
    lastPage = math.ceil(count_all / pageSize)

    #计算上一页 通过 page保存在prePage中
    #设置上一页默认为1
    prePage=1
    #如果当前page大于1 上一页则为page-1
    if page>1:
        prePage=page-1
    #计算下一页
    nextPage=lastPage
    if page < lastPage:
        nextPage = page + 1

   #查看user中所有 \的数据
    #users=db.session.query(Users).all()
    return render_template('10-page.html',users=users,lastPage=lastPage,prePage=prePage,nextPage=nextPage)

@app.route('/14-delete')
def delete_views():

    #接受前端传过来的id
    #删除指定id的对应的元素
    id=request.args.get('id')
    u=Users.query.filter_by(id=id).first()
    db.session.delete(u)
    
    return redirect('/10-page')

@app.route('/15-update',methods=['GET','POST'])
def update_15():
    if request.method == 'GET':

        #请求源地址  并保存给url_ref全局变量
        global url_ref
        url_ref= request.headers.get('Referer')
        print(url_ref)
        #接受id 查询相关数据
        id= request.args.get('id')
        user=Users.query.filter_by(id=id).first()
        #响应给模板
        return render_template('15-update.html',user=user)
    else:
        print("请求源地址"+url_ref)
        #1.接受前端传递过来的数值
        id= request.form['id']
        username=request.form['username']
        age=request.form['age']
        email=request.form['email']
        isActive=False
        if 'isActive'in request.form:
            isActive= True
        #根据id查询对应的user对象
        user= Users.query.filter_by(id=id).first()
        #为user对象重新赋值
        user.username= username
        user.age=age
        user.email=email
        user.isActive=isActive
        #再重新保存对象
        db.session.add(user)
        
    #声明一个全局变量用于接受修改之前的请求原地址‘

        return redirect(url_ref)









####此程序出错！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
@app.route('/12-desc')
def order_by_desc():
    shengxu=db.session.query(Users).order_by(Users.age.desc()).all()
    #shengxu = db.session.query(Users).order_by("age desc,id").all()
    print(shengxu)
    return "聚合排序成功"
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
@app.route('/11-aggregate')
def aggregate():

    de=db.session.query(func.avg(Users.age)).all()
    print(de[0][0])
    print("平均年龄为：%.2f" % (de[0]))
    return "d"

@app.route('/12-juhe')
def juhe():
    # tuple_k=db.session.query(func.avg(Users.age),func.sum(Users.age),func.max(Users.age),func.min(Users.age)).all()
    #
    # print("平均年龄为：%s,总年龄：%s,最大：%s，最小：%s"%(tuple_k[0][0],tuple_k[0][1],tuple_k[0][2],tuple_k[0][3]))

    # 分组聚合 按isActive分组求每组的人数
    #sql: select  isActive,count(*) from users group isActive
    users=db.session.query(Users.isActive,func.count('*')).group_by('isActive').all()
    print(users)
    for r in users:
        print(r[0],":",r[1])
    return  "查询成功"

@app.route('/12-update')
def update_o():
    #1.先查询出id为4的用户信息
    user=Users.query.filter_by(id=4).first()
    #再将其age 改为80
    user.age=31
    #将其保存为数据ku
    db.session.add(user)
    
    return "修改成功"

@app.route('/13-delete')
def delete_o():
    #查询id为4的用户的信息
    user=Users.query.filter_by(id=7).first()
    #删除该信息
    db.session.delete(user)
    
    return "删除成功"



if __name__ == "__main__":
    #app.run(debug=True)
    #通过manager启动服务
    manager.run()

    #通过 manger启动服务
    #python3 run01.py   runserver
    #问题一  无法指定调试模式（debug=True）
    #解决方案  app.config['DEBUG']=True
    #问题二：无法指定启动主机地址（host=0.0.0.0）
    #解决方案  ：  python3 run01.py -- host 0.0.0.0
    #问题三  无法指定启动端口  （post=5555）
    #解决方案  python3 run01.py runserver --port 5555
    #runserver - -host 127.0.0.1 - -port 5000
    #可看 python run.py     python run.py db init
#Target database is not up to date.