from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pandas import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/ajax"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Province(db.Model):
    __tablename__ = "province"
    id = db.Column(db.Integer,primary_key=True)
    pname=db.Column(db.String(30),nullable=False)
    citys= db.relationship(
        "City",
        backref= 'province',
    lazy = 'dynamic'
    )
    def to_dict(self):
        dic={
            "id":self.id,
            "pname":self.pname
        }
        return  dic


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30),nullable=False)
    pid = db.Column(
        db.Integer,
        db.ForeignKey('province.id')
    )
    def to_dict(self):
        dic={
            "id":self.id,
            "pid":self.pid,
            "cname":self.cname

        }
        return dic


@app.route('/05-province')
def lfl():
    provinces = Province.query.all()
    l = []
    for p in provinces:
        l.append(p.to_dict())
    return json.dumps(l)

@app.route("/05-city")
def city_vies():
    pid = request.args['pid']
    cities = City.query.filter_by(pid=pid).all()
    l = []
    for c in cities:
        l.append(c.to_dict())
    return json.dumps(l)







db.create_all()


if __name__ == '__main__':
    app.run(debug=True)



